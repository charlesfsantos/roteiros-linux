## Instalação de interface gráfica: internal-client

Neste guia prático, você fará a instalação das ferramentas necessárias para a execução de uma interface gráfica na VM `internal-client`. Considere, antes de começar, os seguintes aspectos

1. Crie um *snapshot* da máquina `internal-client` antes de ligá-lo.
2. Ao ligar a máquina, se assegure que as máquinas `firewall` e `internal-server` estão em funcionamento. Em seguida, siga as instruções e passos a seguir.

### Passo A: Atualizar e Atualizar o Sistema

1. Teste a conectividade da rede por meio do `firewall`
    * `elinks uol.com.br`

2. Em `internal-client`, Garanta a atualização dos pacotes do sistema:

```
apt update && apt upgrade -y
```

### Passo B: Instalar um Gerenciador de Tela

Para este guia, usaremos o LightDM:

```
apt install lightdm -y
```

Durante a instalação, você pode ser solicitado a selecionar um gerenciador de exibição padrão — escolha LightDM (ou o de sua preferência).

### Passo C: Escolher e Instalar um Ambiente de Desktop
O Debian suporta vários ambientes de desktop. Faremos a instalação do XFCE:

  ```
  apt install xfce4 -y
  ```

Instale os aplicativos comuns (navegador, gerenciador de arquivos, etc.), use a ferramenta `tasksel`:
```
apt install tasksel -y
tasksel
```
Selecione a opção `ambiente da área de trabalho do Debian` com a tecla `SPACE`. Em seguida, `Enter`. 

### Passo D: Configurar e Iniciar a Interface Gráfica
- Habilite o gerenciador de exibição para iniciar na inicialização:
  ```
  systemctl enable lightdm
  ```
- Reinicie o sistema:
  ```
  reboot
  ```

Após a reinicialização, você deve ver uma tela de login gráfica. Faça login com seu nome de usuário e senha para acessar o desktop.

Em seguida, teste a conexão à Internet a partir do navegador. 


