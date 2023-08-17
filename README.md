# PILM
> `PILM` is an acronym to _Parts Inventory Level Monitoring_

- Fábricas
  - Fábrica 1
    - 5 linhas de produção
    - Produz os 5 produtos
    - Lote de 48 produtos por linha
    - Fabricação Empurrada
  - Fábrica 2
    - 8 linhas de produção
    - Produz os 5 produtos
    - Lote e produto variam dependendo dos pedidos do mercado
    - Fabricação Puxada
- Produto
  - 5 versões (Pv1, Pv2, Pv3, Pv4, Pv5).
  - 43 partes bases
  - 20 a 33 novas partes dependendo da versão
- Partes
  - Total de 100 partes diferentes usadas na fabricação
- Monitoramento
  - Nível de estoque de produtos (1 a 5)
  - Lote de fabricação para o dia (lista de partes enviado para almoxarifado)
  - Abastecimento de partes nas linhas
  - Monitoramento de estoques de partes em cada linha para cada parte
    - O estoque de partes deve apontar nível de estoque VERDE, AMARELO, VERMELHO
    - Quando o nível se aproxima do nível vermelho é necessário disparar ordem
    de reabastecimento (MQTT - ordem de compra para o Fornecedor) para o Almoxarifado
