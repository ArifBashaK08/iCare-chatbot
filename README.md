Create a conda environment in the repository
######
conda create -n <App_name> python=<version> -y
######

Activate a conda environment
######
conda activate <App_name>
######

Add below requirements in "requirements.txt" file :

######
sentance-transformers == 2.2.2
lanchain
pypdf
python-dotenv
pinecone[grcp]
langchain-pinecone
langchain-community
langchain-openai
langchain-experimental
######

Bonus tip - You can avoid some issues on Windows by using conda-forge versions when available:
######
conda install -c conda-forge sentencepiece
######

Run below comand in terminal
######
pip install -r requirements.txt
######
