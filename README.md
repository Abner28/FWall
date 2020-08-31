# FWall
Repositório da interface gráfica e dos códigos utilizados no projeto PUB/2019-20.

Atualmente existem três arquivos compondo o projeto: **Galerkin_GUI.py**, **Esteira_GUI.py** e **MAIN.py**.
        
1. **Galerkin_GUI.py**: Responsável pelo cálculo dos valores nodais de circulação.
        
2. **Esteira_GUI.py**: Responsável pelo cálculo da esteira de vórtices, ou também uma alternativa para o cálculo da circulação,
                            utilizando **séries de Fourier.**                  
                            
3. **MAIN.py**: Interface gráfica que facilita o processo de simulação.

# Como utilizar a interface

Em primeiro lugar, abrir o arquivo **MAIN.py** com os demais códigos no mesmo diretório, e executá-lo. 

Ao abrir o programa, deve-se clicar em **New**, e logo após em **New Simulation** para que a janela de simulação se abra.
Nesta janela, deve-se digitar todos os parâmetros desejados e, finalmente, clicar no botão **Run**.

Os gráficos necessários e o valor do coeficiente de sustentação (CL) será apresentado. 

**OBS**: Para simular com outros parâmetros, não é necessário fechar a janela, e sim apenas mudar o parâmetro desejado
e novamente clicar no botão **Run**.

# Descrição dos parâmetros:

1.) **Number of Wings**: Número de asas utilizadas na simulação. Na versão atual são suportadas 1,3 ou 9 asas simultaneamente
(no caso com 3 asas, assume-se 3 asas alinhadas horizontalmente, portanto, z_offset deve ser nulo)

2.) **Wing span**: Envergadura das asas. Como o espelhamento é representado por asas de mesma envergadura que a asa física,
basta entrar a envergadura de uma das asas.

3.) **AoA**: Ângulo de ataque da asa física (quando necessário, o código já utiliza valores negativos para o AoA)

4.) **y_offset**: Fator de offset na direção y. Suponha que escolha-se 3 asas para a simulação. Se y_offset = 1.1, 
as asas à direta e à esquerda estarão posicionadas à uma distancia entre centros de 1.1*span com relação à asa central.

5.) **z_offset**: Diferentemente de y_offset, o valor colocado em z_offset representará a distância entre asas na direção
z, isto é, se z_offset = 6, quer dizer que a distância entre asas em z será 6, tanto as asas superiores quanto inferiores.

6.) **Element type**: Por padrão, "LL2" ou "ll2"

7.) **Mesh type**: Na atual versão, apenas "uniform" disponível.

8.) **Plot figures together**: Se "True", gera um gráfico das posições das asas juntamente com a distribuição de circulação.
Do contrário (False), gerará dois gráficos, um para a posição e outro para a distribuição de circulação.

9.) **Wing Type**: O código possui suporte para asas flexíveis e planas. Entretanto, na atual versão, recomenda-se o uso de
asas flexíveis apenas quando o número de asas for 1, para fins de comparação com uma asa planar.

10.) **Number of elements**: Número de subdivisões da envergadura (discretização). Nesse caso, o número de nós sobre a asa
será dado por **(Number of elements + 1)**.

11.) **r**: Fator de discretização. Nos relatórios utilizou-se **r = 0.1 **.

12.) **Uinf**: Velocidade do escoamento
