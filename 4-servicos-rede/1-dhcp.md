## Configuração de Servidor DHCP no Ubuntu/Debian Usando Kea

Nesta prática, iremos configurar, na VM designada como servcidor interno, o serviço DHCP usando o `Kea`, uma solução que substitui o antigo `isc-dhcp-server`. O Kea é configurado por meio de arquivos no formato JSON. O cenário é o mesmo das VMs anteriores:

- **VM1 (firewall)**: Controla o acesso à rede das máquinas internas. Possui IP interno configurado de forma estática. Atua como gateway para a internet, com duas interfaces de rede: uma externa (conectada à internet) e uma interna (para a rede local).
- **VM2 (internal-server)**: Hospeda os serviços de rede, incluindo o DHCP. Configuraremos o Kea aqui para atribuir IPs dinâmicos na rede interna.
- **VM3 (internal-client)**: Máquina para testar os serviços de rede e o acesso à internet via VM1.

#### Pressupostos do Cenário
- Rede interna: Sub-rede 192.168.1.0/24.
  - IP estático da interface interna de VM1: 192.168.1.1 (gateway).
  - IP estático de VM2: 192.168.1.2 (configurado manualmente).
  - Faixa de IPs DHCP: 192.168.1.100 a 192.168.1.200.
- Interfaces de rede:
  - VM1: enp0s3 (externa, para internet) e enp0s8 (interna, para rede local).
  - VM2 e VM3: enp0s3 (interna).
- VM1 já deve ter encaminhamento de pacotes (IP forwarding) e NAT configurados para permitir acesso à internet das VMs internas (realizado na prática anterior).

### Passo A: Configuração Inicial em Todas as VMs
Atualize os pacotes em todas as VMs para evitar problemas de dependências.

Em cada VM (VM1, VM2, VM3), execute como root:
```
$ apt update
```

### Passo B: Configurar DNS estático em internal-server
Devido o `internal-server` hospedar o serviço de DHCP, as configurações de rede deste host precisam ser estáticas. Isso inclui a configuração do DNS padrão, conforme os passos a seguir.

1. Edite `/etc/resolv.conf`:
```
$ vim /etc/resolv.conf
```

2. Atribua os serviços de DNS do Google:
```
nameserver 8.8.8.8
nameserver 8.8.4.4
```

3. Proteja o arquivo contra reescrita
```
$ chattr +i /etc/resolv.conf
```

### Passo C: Instalar e Configurar o Servidor Kea em internal-server

**OBS**: Todos os itens deste do **Passo C** são realizados em **internal-server**.

1. Instale o pacote Kea para DHCPv4:
```
$ apt install kea-dhcp4-server -y
```

2. Faça um *backup* do arquivo principal de configuração do serviço. 

* **ATENÇÃO: o nome do arquivo de backup começa com bkp**:

```
$ cp /etc/kea/kea-dhcp4.conf /etc/kea/bkp_kea-dhcp4.conf
```

3. Certifique-se que o arquivo *backup* foi criado:

```
$ kea-dhcp4 -t /etc/kea/bkp_kea-dhcp4.conf
```

* O retorno da mensagem varia, mas pode conter as seguintes informações:

```
2025-09-23 14:32:15.127 WARN  [kea-dhcp4.cfgmgr] DHCP4_CONFIG_SYNTAX_WARNING [...]
2025-09-23 14:32:15.130 INFO  [kea-dhcp4.hosts] HOSTS_BACKENDS_REGISTERED [...]
2025-09-23 14:32:15.132 INFO  [kea-dhcp4.dhcpsrv] DHCPSRV_CFGMGR_NEW_SUBNET4 [...]

ENTRE OUTRAS MENSAGENS
```

4. Certifique-se, mais uma vez, de que o arquivo *backup* foi criado:

```
$ ls /etc/kea
kea-dhcp4.conf  bkp_kea-dhcp4.conf
```

5. Remova o arquivo original:
```
$ rm /etc/kea/kea-dhcp4.conf
```

6. Considerando que o `vim` cria o arquivo automaticamente na primeira edição, crie e edite o arquivo `/etc/kea/kea-dhcp4.conf`:
```
$ vim /etc/kea/kea-dhcp4.conf
```

7. Aplique as seguintes configurações ao arquivo.

```json
{
  "Dhcp4": {
    "interfaces-config": {
      "interfaces": [ "enp0s3" ]
    },
    "subnet4": [
      {
        "id": 1,
        "subnet": "192.168.1.0/24",
        "pools": [
          {
            "pool": "192.168.1.100 - 192.168.1.200"
          }
        ],
        "option-data": [
          {
            "name": "routers",
            "data": "192.168.1.1"
          },
          {
            "name": "domain-name-servers",
            "data": "8.8.8.8, 8.8.4.4",
            "csv-format": true
          },
          {
            "name": "domain-name",
            "data": "adeilton-cruz.local" # é óbvio q vc VAI colocar seu nome aqui, mais óbvio ainda q vc NÃO vai colocar este comentario que eu escrevi. Só p/ vc ficar mais esperto...
          }
        ]
      }
    ]
  }
}
```

8. Valide a configuração:
```
$ kea-dhcp4 -t /etc/kea/kea-dhcp4.conf
```

* **ATENÇÃO**: o comando deve retornar uma saída semelhante a que foi retratada no item 3. Não pode haver mensagens do tipo **ERROR**, apenas **INFO** e **WARN**, a depender da mensagem. 
* **CASO HAJA MENSAGEM DO TIPO ERROR**: analise o erro conforme a a mensagem indica. Ao final da linha, é informado aonde está a inconsistência (exemplo `/etc/kea/kea-dhcp4.conf:22:14` indica que o erro está na 22ª linha, aproximadamente no caractere 14). Então, retorne para o item 7 e modifique o que for necessário. 

9. Inicie e habilite o serviço:
```
$ systemctl restart kea-dhcp4-server
```

10. Verifique o status do serviço:
```
$ systemctl status kea-dhcp4-server
```
11. Se houver erros, cheque logs com `journalctl -u isc-kea-dhcp4-server` e siga as instruções de atenção do passo 8.

12. Se não houver erros, siga para o **Passo D**.

### Passo D: Configurar internal-client para Usar DHCP

**OBS:** Todos os itens do **Passo D** são executados em **internal-client**.

internal-client deve obter IP via DHCP automaticamente, ao invés de configurá-lo manualmente via arquivo de interfaces. Para isto, modifique o arquivo seguindo os passos abaixo:

1. Edite `/etc/network/interfaces`:
```
$ vim /etc/network/interfaces
```

2. **Apague** as linhas que contém:
```
address 192.168.1.10
netmask 255.255.255.0
gateway 192.168.1.1
```

3. Modifique o modo de obtenção de endereços de `static` para `dhcp` na interface `enp0s3`:
```
$ auto enp0s3
$ iface enp0s3 inet dhcp
```

4. Reinicie a rede:
```
$ systemctl restart networking.service
```

5. Verifique o IP obtido (**daqui em diante, caso seja apresentado algum erro ou saídas diferentes das esperadas, volte para o item 1. deste Passo**):
```
$ ip addr show enp0s3
```

6. Deve mostrar um IP na faixa 192.168.1.100-200.

```
[...]
inet 192.168.1.100/24 brd 192.168.1.255 scope global [..]
[...]
```

7. Verifique o endereço de *gateway*:
```
$ ip route
default via 192.168.1.1 dev enp0s3
[...]
```

8. Verifique se o endereço de DNS foi configurado conforme esperado
```
$ cat /etc/resolv.conf
domain adeilton-cruz.local # mas é óbvio que vai estar seu nome aqui...
search adeilton-cruz.local # aqui também
nameserver 8.8.8.8
nameserver 8.8.4.4
```

### Passo E: Testes no Cenário
1. **Em internal-client, teste DHCP**:
   - Verifique lease: `cat /var/lib/dhcp/dhclient.enp0s3.leases`

2. **Em internal-server, monitore leases DHCP**:
   - Veja leases atribuídos: `cat /var/lib/kea/dhcp4.leases`

3. **Teste acesso à internet via firewall**:
   - Em internal-client: `ping 8.8.8.8` (teste conectividade IP).
   - `ping google.com` (teste DNS).
   - `elinks uol.com.br`

**OBS**: caso haja qualquer falha no teste, repita os itens
  * Todos do **Passo B**.
  * A partir do item 3. do **Passo C**.
  * Todos do **Passo D**. 
