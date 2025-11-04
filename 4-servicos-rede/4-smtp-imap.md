# Prática Guiada: Configuração de Servidor SMTP-IMAP em Debian

Nesta prática, realizaremos a configuração do serviço de e-mail em `internal-server`. Para isso, será configurado o Postfix como servidor **SMTP** e o Dovecot como servidor **IMAP**, pois atuam, respectivamente, no envio e recebimento de correios eletrônicos.  

**Pré-requisitos:**  
- As três VMs (firewall, internal-server e internal-client) estão configuradas no seu domínio (exemplo: `gabriel-fernandes.local`).  
- O `internal-server` já possui serviços como **Kea DHCP** e **Bind9 DNS** instalados e funcionando.  
- As demais práticas anteriores devem ter sido concluídas com sucesso. 
- Faça o *snapshot* da máquina `internal-server` para esta prática. 
- Verifique a conexão com a Internet a partir do `firewall` usando `elinks`. 

---

## Passo A: Atualização do Sistema e Instalação dos Pacotes no `internal-server`

Acesse o `internal-server` via terminal.

1. Atualize o sistema:
   ```bash
   apt update && apt upgrade -y
   ```

2. Instale o Postfix, Dovecot e ferramentas auxiliares:
   ```bash
   apt install postfix dovecot-core dovecot-imapd mailutils -y
   ```

   > Durante a instalação do **Postfix**, selecione **"Site da Internet"** e defina o nome do sistema como `gabriel-fernandes.local` (não esqueça de inserir o **seu domínio**).

---

## Passo B: Configuração do Hostname e Arquivo `/etc/hosts` no `internal-server`

<!-- 1. Defina o hostname completo:
   ```bash
   hostnamectl set-hostname internal-server.gabriel-fernandes.local
   ``` -->

1. Edite `/etc/hosts` para incluir o alias de e-mail:
   ```bash
   vim /etc/hosts
   ```
   Adicione ou ajuste:
   ```
   127.0.0.1       localhost
   127.0.0.1       internal-server
   192.168.1.1     internal-server.gabriel-fernandes.local internal-server mail.gabriel-fernandes.local
   ```

2. Crie o arquivo `/etc/mailname`:
   ```bash
   echo "gabriel-fernandes.local" | tee /etc/mailname
   ```

---

## Passo C: Configuração do Registro MX e Host A no Bind9 (DNS)

O registro **MX** indica qual servidor é responsável pelo recebimento de e-mails do domínio. O host **A** resolve o nome `mail.gabriel-fernandes.local`.

1. Edite o arquivo da zona:
   ```bash
   vim /etc/bind/db.gabriel-fernandes.local
   ```

2. Adicione ou modifique as seguintes linhas no final da seção de registros (não precisa inserir os comentários):
   ```dns
   ; Registro A para o servidor de e-mail
   mail            IN  CNAME  internal-server

   ; Registro MX para o domínio (prioridade 10)
   @               IN  MX  10  mail
   ```
   > O `@` representa o domínio raiz (`gabriel-fernandes.local`).

3. **Atualize o número de série (serial)** da zona (ex: incremente em 1):
   ```dns
   2025110401    ; Serial (exemplo: YYYYMMDD + número do dia)
   ```

5. Verifique a sintaxe do arquivo:
   ```bash
   named-checkzone gabriel-fernandes.local /etc/bind/db.gabriel-fernandes.local
   ```

6. Reinicie o Bind9:
   ```bash
   systemctl restart bind9
   ```

7. Teste a resolução DNS localmente:
   ```bash
   dig @1localhost MX gabriel-fernandes.local
   dig @localhost mail.gabriel-fernandes.local
   ```
   > Você deve ver o registro MX apontando para `mail.gabriel-fernandes.local` e o A com o IP correto.

---

## Passo D: Configuração do Postfix (SMTP) no `internal-server`

1. Edite o arquivo principal:
   ```bash
   vim /etc/postfix/main.cf
   ```

2. Certifique-se de que as seguintes linhas estejam presentes (ou adicione/modifique):
   ```ini
   myhostname = mail
   myorigin = /etc/mailname
   mydestination = $myhostname, gabriel-fernandes.local, localhost, localhost.localdomain, localhost
   mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128 192.168.1.0/24
   mailbox_size_limit = 0
   recipient_delimiter = +
   inet_interfaces = all
   inet_protocols = all
   ```

3. Reinicie o serviço:
   ```bash
   systemctl restart postfix
   ```

4. Teste envio local para um usuário já cadastrado no sistema:
   ```bash
   echo "Teste SMTP local" | mail -s "Assunto Teste" gabriel@gabriel-fernandes.local
   ```
   ````text
   # su - gabriel
   $ mail
   "/var/mail/gabriel": 1 mensagem 1 nova
   N  1 root      ter nov 4 14:50   16/516   Assunto Teste
   ? 1
   ? exit
   $ exit
   ````

---

## Passo F: Testes no `internal-client` via Interface Gráfica

1. Abra o terminal no `internal-client` e instale o Thunderbird:
   ```bash
   apt update && apt install thunderbird -y
   ```

2. Abra o **Thunderbird** pelo menu KDE.

3. Configure a conta:
   - **Nome:** Gabriel Fernandes  
   - **E-mail:** `gabriel@gabriel-fernandes.local`  
   - **Senha:** ifrn  
   - Clique em **Configuração Manual**

   Se a configuração estiver correta, o Thunderbird irá exibir as configurações principais do IMAP com o endereço do servidor configurado. 
   
4. Caso a configuração anterior for positiva, clique em `Done`. 

5. Se uma janela para adicionar exceção de segurança aparecer, clique em `Confirm Security Exception`. 

6. Envie um e-mail para si mesmo e verifique a caixa de entrada.

---

**Conclusão:**  
O servidor de e-mail está configurado com os serviços de e-mail SMTP (com Postfix) e IMAP (com Dovecot). O cliente gráfico no `internal-client` acessa o e-mail através do `internal-server`.
