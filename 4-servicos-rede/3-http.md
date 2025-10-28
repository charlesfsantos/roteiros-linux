# Configuração do Serviço *Web* com Apache HTTP Server

Nesta prática, será realizada a instalação do servidor *web* HTTP Apache em `internal-server`. Neste exemplo, consideraremos o domínio DNS `fabiana-rodrigues.local` que configuramos no serviço de DNS.

Antes de configurar o serviço propriamente dito, adicionaremos um registro CNAME `www` para `internal-server.fabiana-rodrigues.local`. Então, faremos a configuração de dois *websites* no mesmo servidor:

1. Será acessado pelo endereço `internal-server.fabiana-rodrigues.local`. Servirá como uma página de testes do servidor.
2. Consistirá em uma página pessoal que contém informações simples sobre o aluno. O acesso se dará por meio do endereço `www.fabiana-rodrigues.local`.

---

### **Pré-requisitos**
- **Domínio DNS**: `fabiana-rodrigues.local` já configurado no Bind9 em `internal-server`.
- **Registros DNS Existentes** (em `/etc/bind/db.fabiana-rodrigues.local`):
  ```bind
  firewall        IN  A   192.168.1.1
  internal-server IN  A   192.168.1.2
  ```
- **Finalização de todas as práticas anteriores**.

---

## **Passo A: Instalação do Apache2 em internal-server**
1. Acesse `internal-server` via terminal.
2. Atualize os pacotes do sistema:
   ```bash
   apt update && apt upgrade -y
   ```
3. Instale o Apache2:
   ```bash
   apt install apache2 -y
   ```
4. Verifique **se o Apache2 está ativo**:
   ```bash
   systemctl status apache2
   q
   ```
   - **Se não estiver ativo**, inicie-o:
     ```bash
     systemctl start apache2
     ```
   - Habilite o serviço para iniciar automaticamente no boot:
     ```bash
     systemctl enable apache2
     ```

---

## **Passo B: Configuração do Registro CNAME no Bind9**
Um registro CNAME é a melhor solução para `www.fabiana-rodrigues.local`, pois permite que o subdomínio `www` seja um *alias* (isto é, um apelido/redirecionamento) para `internal-server.fabiana-rodrigues.local`, simplificando a manutenção do DNS.

1. Acesse a VM2 e edite o arquivo de zona do Bind9:
   ```bash
   vim /etc/bind/db.fabiana-rodrigues.local
   ```
2. Adicione o registro CNAME ao final do arquivo:
   ```bind
   www  IN  CNAME  internal-server
   ```

   Exemplo do arquivo completo:
   ```bind
   $TTL    604800
   @       IN      SOA     fabiana-rodrigues.local. root.fabiana-rodrigues.local. (
                              2025102801         ; Serial: atualize com a data de hoje
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
   ;
   @       IN      NS      internal-server.fabiana-rodrigues.local.
   firewall        IN  A   192.168.1.1
   internal-server IN  A   192.168.1.2
   www             IN  CNAME  internal-server
   ```

3. Verifique a sintaxe do arquivo de zona:
   ```bash
   named-checkzone fabiana-rodrigues.local /etc/bind/db.fabiana-rodrigues.local
   ```
   - Se aparecer `OK`, a configuração está correta.

4. Reinicie o Bind9:
   ```bash
   systemctl restart bind9
   ```

5. Teste a resolução do nome em internal-server:
   ```bash
   nslookup www.fabiana-rodrigues.local localhost
   ```
   - Deve mostrar que `www.fabiana-rodrigues.local` resolve para `internal-server.fabiana-rodrigues.local` (IP `192.168.1.2`).

---

## **Passo C: Configuração dos Virtual Hosts no Apache2**
Vamos criar dois *virtual hosts*: um para a página de teste e outro para a página pessoal.

1. **Criar os Diretórios para os Sites**
   - Crie os diretórios para os arquivos dos sites:
     ```bash
     mkdir -p /var/www/internal-server.fabiana-rodrigues.local
     mkdir -p /var/www/www.fabiana-rodrigues.local
     ```

2. **Criar a Página de Teste**
   - Crie um arquivo HTML para `internal-server.fabiana-rodrigues.local`:
     ```bash
     vim /var/www/internal-server.fabiana-rodrigues.local/index.html
     ```
     Adicione:
     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <title>Teste do Apache2</title>
     </head>
     <body>
         <h1>Internal Server - Apache2</h1>
         <p>Este é um site de teste para confirmar que o Apache2 está funcionando corretamente!</p>
     </body>
     </html>
     ```
     Salve e feche.

3. **Criar a Página Pessoal**
   - Crie um arquivo HTML para `www.fabiana-rodrigues.local`:
     ```bash
     vim /var/www/www.fabiana-rodrigues.local/index.html
     ```
     Adicione (personalize conforme desejado):
     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <title>Página Pessoal de Fabiana Rodrigues</title>
     </head>
     <body>
         <h1>Bem-vindo à Minha Página Pessoal!</h1>
         <p>Olá, meu nome é Fabiana Rodrigues. Esta é minha página pessoal hospedada no Apache2!</p>
         <p>Sou estudante e estou aprendendo a configurar servidores Linux.</p>
     </body>
     </html>
     ```
     Salve e feche.

4. **Ajustar Permissões**
   ```bash
   chown -R www-data:www-data /var/www/internal-server.fabiana-rodrigues.local
   chown -R www-data:www-data /var/www/www.fabiana-rodrigues.local
   chmod -R 755 /var/www/internal-server.fabiana-rodrigues.local
   chmod -R 755 /var/www/www.fabiana-rodrigues.local
   ```

5. **Configurar os Virtual Hosts**
   - Para `internal-server.fabiana-rodrigues.local`:
     ```bash
     vim /etc/apache2/sites-available/internal-server.fabiana-rodrigues.local.conf
     ```
     Adicione:
     ```apache
     <VirtualHost *:80>
         ServerName internal-server.fabiana-rodrigues.local
         DocumentRoot /var/www/internal-server.fabiana-rodrigues.local
         ErrorLog ${APACHE_LOG_DIR}/internal-server.fabiana-rodrigues.local_error.log
         CustomLog ${APACHE_LOG_DIR}/internal-server.fabiana-rodrigues.local_access.log combined
     </VirtualHost>
     ```
     Salve e feche.

   - Para `www.fabiana-rodrigues.local`:
     ```bash
     vim /etc/apache2/sites-available/www.fabiana-rodrigues.local.conf
     ```
     Adicione:
     ```apache
     <VirtualHost *:80>
         ServerName www.fabiana-rodrigues.local
         DocumentRoot /var/www/www.fabiana-rodrigues.local
         ErrorLog ${APACHE_LOG_DIR}/www.fabiana-rodrigues.local_error.log
         CustomLog ${APACHE_LOG_DIR}/www.fabiana-rodrigues.local_access.log combined
     </VirtualHost>
     ```
     Salve e feche.

6. **Habilitar os Virtual Hosts**
   ```bash
   a2ensite internal-server.fabiana-rodrigues.local.conf
   a2ensite www.fabiana-rodrigues.local.conf
   ```

7. **Desativar o Site Padrão (opcional)**
   ```bash
   a2dissite 000-default.conf
   ```

8. **Testar e Reiniciar o Apache2**
   ```bash
   root@internal-server$ apache2ctl configtest
   
   [...]
   
   Syntax OK
   root@internal-server$ systemctl restart apache2
   ```

---

## **Passo D: Testes em internal-client**
1. Acesse o navegador *web*
2. Insira, na barra de endereços:
    * internal-server.fabiana-rodrigues.local
    * www.fabiana-rodrigues.local
3. Verifique as páginas que aparecem como resultado

## **Passo E: Caso o passo D não funcione**
Entre com `Ctrl direito + F2` em `internal-client` e prossiga com o passo a seguir.

1. **Teste de DNS**:
   - `nslookup www.fabiana-rodrigues.local`
   - Se o endereço IP `192.168.1.2` não aparecer como resposta, volte ao **passo B** e verifique as configurações.
   - Se, por outro lado, o comando for bem sucedido, volte ao **passo C** para verificar as configurações.
---