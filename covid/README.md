## Projet BIF 2020 -- Mapping de données de séquençage COVID

Claire Lemaitre et Téo Lemane



## Données

* `reads.fasta` : un fichier de 10000 reads d'un vrai séquençage d'un échantillon d'un patient atteint de la covid-19, id = SRX9435498 (sous-ensemble, un peu re-formaté, voir ci-dessous)
* `genome_reference.fasta` : le génome de référence du virus sars-cov2, taille = 29903 bp, id = MN908947
* `genome_distant.fasta` : le génome d'un autre betacoronavirus, celui de la chauve-souris, id = MG772933



Ce dossier contient également 2 scripts python (`subsample_and_clean_reads.py` et `fasta1line.py` ) qui ont été utilisés pour mettre les données brutes dans un format plus facile à utiliser. (pour votre information, vous n'en avez pas besoin pour le projet)



## D'où viennent ces données ?

* Données de séquençage [SRX9435498](https://www.ncbi.nlm.nih.gov/sra/?term=SRX9500342) : 
  * Origine : fichier soumis par le  New Mexico Department of Health Scientific Laboratory le 4 novembre 2020
  * Echantillon : prélèvement sur un patient atteint du COVID au Nouveau mexique (USA), le 24/08/2020.
  * Technologie : séquençage Illumina sur une librairie tiled-amplicon (amplification spécifique du génome viral sars-cov2)
  * Lien download : https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?exp=SRX9435498&cmd=search&m=downloads&s=seq
  * Fichier fasta complet : 163 Mo, 556,596 paires de reads de tailles variables (max 150)
  * Fichier `reads.fasta` = sous-échantillonnage de 10000 reads de taille au moins 100 bp sans autre caractère que A, C, G, et T, en évitant les 50000 premiers, et renommage des headers (script python  `subsample_and_clean_reads.py`).
* Génome de référence : sars-cov2, première version du génome de référence (janv 2020)

  * Publication : Wu et al , Feb 2020 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7094943/
* ID : MN908947 :https://www.ncbi.nlm.nih.gov/nuccore/MN908947
  * Modification : formate pour mettre toute la séquence sur une seule ligne (script python `fasta1line.py`)
* Génome distant : betacoronavirus identifié chez la chauve-souris :
  * Publication : Wu et al , Feb 2020 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7094943/
  * ID = MG772933 : https://www.ncbi.nlm.nih.gov/nuccore/MG772933
  * Distance avec le sars-cov2 : 89.1% id d'après la publication Wu et al, 2020.
  * Modification : formate pour mettre toute la séquence sur une seule ligne (script python `fasta1line.py`)



## Résultats attendus

Les données de séquençage ont été obtenues après amplification de l'ARN viral (contrairement à des données de type "méta-transcritomique" qui peuvent contenir des proportions importantes d'ARN de l'hôte ou d'autres microbes). On s'attend donc à ce que plus de 95% des reads proviennent bien du sars-cov2. Le génome de référence MN908947 est celui du sars-cov2 assemblé en janvier 2020, à partir d'un prélèvement sur un patient de la région de Wuhan en Chine. Le séquençage SRX9435498 est celui d'un autre patient, provenant d'une autre région géographique (USA), donc contient probablement une autre souche du sars-cov2, mais le prélèvement date d'août 2020, soit environ 8 mois après. On s'attend à peu de mutations entre ces deux souches (maximum une trentaine). Donc, la majorité des reads devraient être mappés sur le génome de référence avec pas ou peu de différences.

Si on utilise le génome du betacoronavirus infectant les chauves-souris, le résultat de mapping devrait être bien différent...



## Comment a-t-on récupéré ces données (ou d'autres) ?

* Génomes de référence :

  ```
  Aller sur le site : https://www.ncbi.nlm.nih.gov/
  Dans le champ de recherche, mettre l'ID : MN908947 puis "Search"
  en haut à droite : "Send to" -> File -> Format FASTA
  ```

  Formatage :

  ```
  python fasta1line.py temp.fasta > genome_reference.fasta
  ```

  

* Données de séquençage :

  ```
  Aller sur le site : https://www.ncbi.nlm.nih.gov/sars-cov-2/
  "SARS-CoV-2 next-generation sequencing runs in SRA" -> cliquer sur "View in SRA"
  On arrive sur : https://www.ncbi.nlm.nih.gov/sra/?term=txid2697049%5BOrganism:noexp%5D%20NOT%200[Mbases]
  Filtrer (colonne à gauche) : Platform = "Illumina"
  J'ai choisi le premier, avec le mot "Amplification" dans le titre (au hasard)
  Sinon : dans le champ de recherche : mettre SRX9500342 puis cliquer sur "Search"
  cliquer sur le Run correspondant : "SRR13050897"
  Sur le site : https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR13050897
  Cliquer dans le menu du haut "Download" -> "FASTA/FASTQ"
  "Experiments" : remettre l'ID "SRX9500342"
  "Download"  (à droite)
  ```

  Sous-échantillonnage, sélection de 10000 reads :

  ```
  python subsample_and_clean_reads.py SRX9500342.fasta > reads.fasta
  ```

  

  Autre site où on peut télécharger des séquences du virus, à l'EBI (européen vs ncbi = USA) :

  https://www.covid19dataportal.org/sequences?db=sra-experiment-covid19#search-content

  Sur ce site, on peut filtrer par l'origine géographique. Il y a quelques jeux de données français, mais ils étaient un peu trop gros pour cette expérience (plusieurs Go chacun).

