# Prática Guiada: Configuração de um Servidor DNS no Debian

Nesta prática, o servidor DNS `bind9` será configurado em `internal-server` para resolver nomes locais em um domínio da rede interna (**exemplo:** domínio "miguel-judson.local") e encaminhar consultas para a internet via *forwarders*. Isso permite que `internal-client` teste os serviços de rede e acesse a internet através do firewall.

**Premissas:**
- Rede interna: 192.168.1.0/24.
- IP de `firewall`, interface interna: 192.168.1.1 (verificar no arquivo `/etc/network/interfaces`).
- IP de `internal-server`: 192.168.1.2 (verificar no arquivo `/etc/network/interfaces`).
- O servidor DHCP está configurado em `internal-server`. Verifique as configurações com:
    * `cat /etc/kea/kea-dhcp4.conf`
    * `kea-dhcp4 -t /etc/kea/kea-dhcp4.conf`
- IP de `internal-client`: Dinâmico via DHCP configurado em `internal-server` (verifique com `ip a`).
- **IMPORTANTE:** Se houverem erros, será necessário verificar as configurações realizadas nos roteiros anteriores. 

**Objetivos:**
- Instalar e configurar o bind9 em internal-server como servidor DNS autoritativo para a rede local.
- Configurar uma zona forward e reverse para resolução de nomes locais.
- Integrar com o DHCP KEA para que os clientes recebam o IP do DNS automaticamente.
- Testar em internal-client.

## Passo A: verificar conectividade com elinks em firewall

Em firewall, execute:

```
elinks uol.com.br
```

Realize a autenticação com sua matrícula do IFRN conforme necesário. Assim que bem sucedido, insira `Ctrl+C` no teclado. 

## Passo B: Atualize o Sistema em internal-server

Em `internal-server`, atualize os pacotes para garantir que tudo esteja atualizado.

```
apt update && apt upgrade -y
```

## Passo C: Instale o bind9 em internal-server
Em `internal-server`, instale o pacote bind9 e ferramentas úteis. 

```
apt install bind9 bind9-utils dnsutils -y
```

- `bind9`: O servidor DNS principal.
- `bind9-utils`: Ferramentas como `named-checkzone` para verificação.
- `dnsutils`: Inclui `dig` e `nslookup` para testes.

Verifique se o serviço está rodando:

```
systemctl status bind9
```

A mensagem deve retornar uma mensagem semelhante à seguinte:

```
● bind9.service - BIND Domain Name Server
     Loaded: loaded (/lib/systemd/system/bind9.service; enabled; preset: enabled)
     Active: active (running) since Mon 2025-10-06 15:02:10 -03; 1h ago
       Docs: man:named(8)
   Main PID: 1234 (named)
      Tasks: 5 (limit: 4660)
     Memory: 10.2M
        CPU: 0.150s
     CGroup: /system.slice/bind9.service
             └─1234 /usr/sbin/named -f -u bind

...
```

Se não estiver, inicie-o:

```
systemctl start bind9
systemctl enable bind9
```

## Passo D: Configure as Opções Gerais do bind9
Edite o arquivo `/etc/bind/named.conf.options` para definir configurações básicas, como *forwarders* para a Internet e restrições de acesso.

Use um editor como vim:

```
vim /etc/bind/named.conf.options
```

Modifique o bloco `options` para que o seguinte trecho (remova os caracteres `//` antes das linhas, caso necessário) destacado fique da seguinte forma:

```
options {
    [...]

    forwarders {
        8.8.8.8;
        8.8.4.4;
    };
    forward only;

    [...]
};
```

- **Explicação:**
  - `forwarders`: Encaminha consultas não locais para servidores DNS externos.
  - `forward-only`: remove sobrecarga do servidor ao dispensar consulta recursiva aos demais servidores DNS. 

Salve e saia da edição do arquivo.

## Passo E: Defina as Zonas Locais
Edite `/etc/bind/named.conf.local` para declarar as zonas (domínios) que o servidor gerenciará.

```
vim /etc/bind/named.conf.local
```

Ao final do arquivo, insira as seguintes zonas (exemplo para domínio `miguel-judson.local`):

```
zone "miguel-judson.local" { // agora você aprendeu...
    type master;
    file "/etc/bind/db.miguel-judson.local";
    allow-update { none; };  // Sem atualizações dinâmicas por agora
};

zone "1.168.192.in-addr.arpa" {
    type master;
    file "/etc/bind/db.192.168.1";
    allow-update { none; };
};
```

- **Explicação:**
  - `miguel-judson.local`: Zona direta para resolução de nomes para IPs (ex: `internal-server.miguel-judson.local` -> `192.168.1.2`).
  - `1.168.192.in-addr.arpa`: Zona reversa para resolução de IPs para nomes (ex: `192.168.1.2` -> `internal-server.miguel-judson.local`).

## Passo F: Crie os Arquivos de Zona
Crie o arquivo de zona direta `/etc/bind/db.miguel-judson.local`:

```
vim /etc/bind/db.miguel-judson.local
```

Conteúdo exemplo (use a data atual no serial, formato YYYYMMDD01):

```
$TTL 604800
@       IN      SOA     internal-server.miguel-judson.local. root.miguel-judson.local. (
                              2025100301 ; Serial (atualize sempre que editar)
                                 604800  ; Refresh
                                  86400  ; Retry
                                2419200  ; Expire
                                 604800 ) ; Negative Cache TTL

@       IN      NS      internal-server.miguel-judson.local.
internal-server     IN      A       192.168.1.2
firewall     IN      A       192.168.1.1
```

Agora, crie o arquivo de zona reverse `/etc/bind/db.192.168.1`:

```
vim /etc/bind/db.192.168.1
```

Conteúdo:

```
$TTL 604800
@       IN      SOA     internal-server.miguel-judson.local. root.miguel-judson.local. (
                              2025100301 ; Serial
                                 604800  ; Refresh
                                  86400  ; Retry
                                2419200  ; Expire
                                 604800 ) ; Negative Cache TTL

@       IN      NS      internal-server.miguel-judson.local.
2       IN      PTR     internal-server.miguel-judson.local.
1       IN      PTR     firewall.miguel-judson.local.
```

- **Explicação:** Os registros PTR são para resolução reversa. 
- Defina permissões corretas:

```
chown bind:bind /etc/bind/db.*
chmod 644 /etc/bind/db.*
```

## Passo G: Verifique a Configuração
Verifique erros na configuração:

1. Verifique o arquivo de configuração do serviço

```
named-checkconf /etc/bind/named.conf
```

Interpretação da Saída:

* Sem saída: Configuração válida
* Saída com erro: verifique a linha onde está localizado o erro:

Exemplo de erro:

```
/etc/bind/named.conf.local:3: missing ';' before '}'
```

Isso significa que há um erro de sintaxe na linha 3 de /etc/bind/named.conf.local (falta um ponto e vírgula antes de um }).

2. Cheque se a sintaxe dos seus arquivos de zona estão corretos:

```
named-checkzone miguel-judson.local /etc/bind/db.miguel-judson.local
```

```
named-checkzone 1.168.192.in-addr.arpa /etc/bind/db.192.168.1
```

Saída esperada:

```
zone miguel-judson.local/IN: loaded serial 2025100301
OK
```

Se OK, reinicie o serviço:

```
systemctl restart bind9
```

Verifique logs para erros:

```
journalctl -u bind9
```

## Passo H: Integre com o DHCP KEA em internal-server
Edite a configuração do KEA (geralmente em `/etc/kea/kea-dhcp4.conf`) para informar o DNS aos clientes.

Modifique o seguinte trecho:

```
"option-data": [
    [...]

    {
        "name": "domain-name-servers",
        "data": "192.168.1.2"
    },

    [...]
]
```

Reinicie o KEA:

```
systemctl restart kea-dhcp4-server
```

## Passo I: Teste em internal-client (Cliente Interno)
Em `internal-client`, renove o IP via DHCP:

```
ifdown enp0s3 && ifup enp0s3
```

Verifique `/etc/resolv.conf` (deve mostrar `nameserver 192.168.1.2`).

Teste resoluções:

- Local: `nslookup internal-server.miguel-judson.local`
- Reverse: `dig -x 192.168.1.2`
- Externo: `dig google.com` (deve usar forwarders)

Teste, a partir de `internal-client`:
-  `elinks uol.com.br`.
