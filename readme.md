Apenas consegui fazer com que o Kong se comunicasse com a API usando o ipv4, portanto, é necessário que no arquivo do caminho Kong/config/kong.yaml (LINHA 55), o host seja alterado para o ipv4 local da máquina onde as aplicações estiverem rodando.

Feito isso, rodar o script start.sh, para que o Kong seja configurado na máquina.

Importar a configuração do Kong do arquivo Kong/config/kong.yaml utilizando o comando "deck sync".

Para instalar os pacotes necessários para que a api rode, execute o seguinte comando:

pip install -r requirements.txt

Para rodar a aplicação, executar o comando:

python app.py

Para testar a aplicação, utilizar o json Teste-integracao-KONG+API, o qual é uma coleção do postman.