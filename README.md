# 🛡️ Escudo Digital Cidadão

[![Status](https://img.shields.io/badge/Status-Online-10b981?style=for-the-badge)](https://escudocidadao.com.br/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web_Framework-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Licença](https://img.shields.io/badge/Licença-MIT-blue?style=for-the-badge)](LICENSE)

O **Escudo Digital Cidadão** é uma plataforma web gratuita e de utilidade pública dedicada à conscientização, prevenção e combate a fraudes virtuais e ataques de engenharia social. Originalmente idealizado como projeto de extensão universitária em Ciência da Computação, o sistema consolidou-se como uma **iniciativa independente e contínua** voltada a proteger cidadãos comuns contra estelionatos digitais.

🌐 **Acesse a plataforma online:** [https://escudocidadao.com.br/](https://escudocidadao.com.br/)

---

## ⚙️ Funcionalidades da Plataforma

A aplicação reúne ferramentas interativas de treinamento, inteligência de fontes abertas (OSINT) e protocolos de resposta rápida a incidentes:

- **📞 Treinamento de Ligações (Simulador Prático):** Quiz interativo baseado em boletins de ocorrência reais que recria abordagens telefônicas fraudulentas (falsa central bancária, roubo de código SMS do WhatsApp, indução à instalação de acesso remoto como AnyDesk, golpe do falso familiar, dentre outros), com barra de progresso, feedback pedagógico imediato e pontuação final.
- **💬 Simulador de Golpes (Interface WhatsApp):** Ambiente imersivo em modo escuro controlado por uma **Máquina de Estados** em JavaScript que simula, em tempo real, a pressão psicológica do *Golpe do Falso Advogado*, incluindo indicador de digitação dinâmico e alerta educativo ao final da interação.
- **🌐 Verificador de Sites (OSINT / WHOIS):** Ferramenta de análise investigativa que sanitiza URLs suspeitas, consulta registros globais via protocolo WHOIS, calcula a idade exata do domínio em dias e classifica o grau de risco (domínios recém-criados ou ocultos recebem alerta imediato de fraude).
- **🚨 O Preço do Golpe (Conscientização e Estatísticas):** Painel informativo sobre os impactos financeiros, jurídicos, familiares e psicológicos dos cibercrimes, catalogando as principais modalidades de golpes no Brasil com dados atualizados da imprensa e órgãos de segurança.
- **📝 Protocolo "Caí no Golpe, O que Faço?":** Guia passo a passo de ação emergencial para vítimas, orientando sobre o acionamento do Mecanismo Especial de Devolução (MED) do PIX, reclamações no Banco Central/Consumidor.gov.br, registro na Delegacia Online, monitoramento no Registrato e preservação técnica de provas digitais (cabeçalhos de e-mail, Wayback Machine e TXID de criptoativos).
- **📥 Cartilha de Proteção Digital (PDF Gratuito):** Disponibilização de material educativo completo em PDF para download gratuito.

---

## 💻 Arquitetura e Tecnologias Utilizadas

O projeto foi estruturado sob uma arquitetura web full-stack, combinando processamento backend em Python, persistência relacional e interface responsiva em tema escuro (*Dark Mode Cyber*):

### Backend & Segurança (OSINT)
- **Python 3 & Flask:** Roteamento web, renderização dinâmica de templates e entrega segura de arquivos (`send_file`).
- **Flask-SQLAlchemy:** Mapeamento objeto-relacional (ORM) para registro de estatísticas de acesso e downloads da cartilha.
- **python-whois & urllib.parse:** Extração de domínios, tratamento de prefixos e consultas automatizadas de metadados de registro (data de criação de domínios).
- **Variáveis de Ambiente (`os.environ`):** Isolamento seguro de credenciais de banco de dados (`DATABASE_URL`) e chaves administrativas (`ADMIN_SENHA`).

### Banco de Dados
- **PostgreSQL:** Banco de dados relacional utilizado em ambiente de produção na nuvem.
- **SQLite:** Banco de dados local automático para testes e desenvolvimento seguro sem interferir nos dados de produção.

### Frontend & UI/UX
- **HTML5 & CSS3:** Estilização moderna em tema escuro com efeitos de *glassmorphism*, gradientes e animações suaves.
- **Bootstrap 5.3:** Estruturação responsiva em abas (*pills*), modais e componentes adaptáveis a dispositivos móveis e desktops.
- **JavaScript (ES6+):** Motor lógico do simulador de WhatsApp (árvore de decisão e manipulação de DOM), lógica do quiz de ligações e persistência local de preferências de privacidade.
- **Jinja2:** Integração dinâmica entre os resultados das análises WHOIS no Python e os alertas visuais no HTML.

### Infraestrutura, Domínio & SEO
- **Render:** Hospedagem em nuvem com deploy contínuo integrado ao GitHub.
- **Cron-Job:** Monitoramento automatizado de disponibilidade (*uptime*) para manter a aplicação ativa.
- **Registro.br:** Domínio nacional oficial (`escudocidadao.com.br`).
- **Git & GitHub:** Controle de versão e histórico de evolução do código-fonte.

---

## 🔍 Propósito e Impacto Social

O **Escudo Digital Cidadão** nasceu da necessidade de traduzir conhecimentos técnicos de cibersegurança e investigação digital em ferramentas práticas e acessíveis para toda a população. Ao combinar educação preventiva com verificação automatizada de domínios suspeitos, a plataforma atua como uma linha de defesa gratuita e permanente contra fraudes financeiras e engenharia social.

---


## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para estudar, propor melhorias e compartilhar a iniciativa para ajudar mais pessoas a se protegerem na internet.

---

**Desenvolvido e mantido por Ronieryson Pereira Virginio**
- Oficial Investigador de Polícia Civil - [PCES]
- Estudante de Ciência da Computação
- Pós-Graduado em Big Data e Inteligência Artificial
- Graduado em Ciências Contábeis