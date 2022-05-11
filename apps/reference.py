import streamlit as st

def app():
    st.title("Notas e Referências")

    text = '''
    Olá, seja bem-vindo ao dashboard de monitoramento de qualidade do ar.


    Todos os dados podem ser acessados pela [Plataforma IEMA](https://energiaeambiente.org.br/qualidadedoar). 
    Caso tenha interesse de estar obtendo os dados mais recentes, os dados podem ser baixados e realizados.

    As análises estatísticas apresentados ao longo do dashboard fornecem uma visão mais direta quanto ao dados.
    Os testes utilizados foram Testes-t, ANOVA e Correlações. Como os dados não possuem uma distribuição normal, 
    ou podem eventualmente falhar nas premissas báscias dos testes frequentistas não paramétricos, estamos empregando
    as formas não paramétricas de todos eles. Para o teste-t estamos utilizando [Wilcoxon](https://pingouin-stats.org/generated/pingouin.wilcoxon.html#pingouin.wilcoxon), para a ANOVA estamos
    utilizando o [Kruskal-Wallis](https://pingouin-stats.org/generated/pingouin.kruskal.html#pingouin.kruskal), 
    e as correlações são utilizanod o método de [Shepherd](https://pingouin-stats.org/generated/pingouin.corr.html#pingouin.corr).

    Todas as [múltiplas comparações](https://pingouin-stats.org/generated/pingouin.multicomp.html#pingouin.multicomp) 
    tiveram seu p-valor corrigido utilizando o método de Holm. Este método foi escolhido uma vez que impõe uma penalização 
    tão boa quanto o método de Bonferroni, porém sem ser tão conservador. 

    Por fim, vale notar que existe uma quantia muito grande de dados e, por conta disso, os testes podem dar todos
    siginificativos a um nível de significância de 5%. Como no trabalho de [Karmer et al. (2014)](https://doi.org/10.1073/pnas.1320040111),
    o p-valor puro poderia nos levar a interpretar de maneira errônea os dados e, pensando nisso, incluímos também
    os tamanhos de efeito. As _rules of thumb_ dos tamanhos de efeito são explanadas pela [Universidade de Cambridge](https://imaging.mrc-cbu.cam.ac.uk/statswiki/FAQ/effectSize).
    '''

    for sentence in text.split('\n\n'):
        st.write(sentence)