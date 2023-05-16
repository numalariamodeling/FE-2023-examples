# FE-2023-examples
Exemples de scripts pour le programme d'enrichissement de la faculté de 2023 sur la modélisation appliquée du paludisme à Northwestern

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.md)
[![fr](https://img.shields.io/badge/lang-fr-red.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.fr.md)


### Voie technique (EMOD)

**Vue d'ensemble:**
Les exercices consistent généralement en une simulation et un analyseur des résultats de la simulation. Dans certaines semaines, des scripts supplémentaires existent pour préparer les entrées de simulation ou générer des sorties et des tracés supplémentaires, ou pour la calibration du modèle, comme décrit dans les instructions pour les semaines respectives.

**Scripts fournis et vérification des résultats :**.
Quelques scripts principaux sont fournis au niveau principal de ce référentiel, y compris des exemples d'exécution et des analyseurs. La majeure partie du travail pour ce cours sera effectuée par vous en construisant vos propres scripts basés sur les instructions avec l'aide de ces scripts. Pour chaque semaine, des scripts de simulation suggérés à des fins de comparaison ou d'aide pendant l'exercice sont fournis dans le dossier [solution scripts](https://github.com/numalariamodeling/FE-2023-examples/tree/main/solution_scripts) de la semaine concernée. Les scripts de solution contiennent également un fichier de collection d'analyseurs qui comprend de nombreux analyseurs couramment utilisés et que vous pourriez vouloir explorer plus en profondeur dans le cadre de votre projet. 

*Note: si vous utilisez un analyseur de la collection, assurez-vous d'ajouter les rapporteurs appropriés pour créer les fichiers de sortie nécessaires.*

**Prérequis:** 
Avant d'exécuter les scripts d'exemple hebdomadaires, veuillez vous assurer que l'environnement virtuel emodpy a été [installé](https://numalariamodeling.github.io/FE-2023-quarto-website/guides/install_guide.html) et que ce [référentiel a été cloné](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) dans votre répertoire personnel sur QUEST, idéalement sous la forme _/home/<.username>/FE-2023-examples_. L'exécution de vos scripts nécessitera le chargement de l'environnement virtuel emodpy et suppose que les fichiers soient exécutés à partir d'un répertoire de travail situé à l'endroit où se trouve le script. Sur QUEST, il existe un environnement virtuel qui peut être chargé en utilisant `source activate /projects/b1139/environments/emodpy_alt` - cet environnement utilise la plate-forme idmtools `SLURM_LOCAL`. Avant de commencer un exercice, assurez-vous que vous avez extrait ou récupéré les derniers changements du dépôt (voir git-guides [git-pull](https://github.com/git-guides/git-pull)).

Vous devrez également configurer votre fichier `.bashrc` (situé dans votre répertoire personnel). Nous utilisons ce fichier pour charger automatiquement les modules, tels que python, qui sont nécessaires au fonctionnement d'EMOD. Nous pouvons également inclure un alias pour l'environnement virtuel décrit ci-dessus. Le modèle ci-dessous crée une commande alias appelée `load_emodpy` que nous pouvons exécuter dans le terminal pour activer l'environnement - elle utilise la même commande que celle mentionnée ci-dessus. Vous pouvez utiliser ce même alias ou en créer un autre pour votre environnement virtuel personnel si vous le souhaitez.

Cliquez sur la flèche pour agrandir :
<details><summary><span><em>Modèle de fichier `.bashrc`</em></span></summary>
<p>

Ce modèle peut être copié directement dans votre fichier `.bashrc` sur QUEST:

```bash
# .bashrc

# Définitions globales des sources
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Décommentez la ligne suivante si vous n'aimez pas la fonction de recherche automatique de systemctl:
# export SYSTEMD_PAGER=

# Alias et fonctions spécifiques à l'utilisateur
alias load_emodpy='source activate /projects/b1139/environments/emodpy_alt'
module purge all
module load singularity/3.8.1
module load git/2.8.2
module load python/3.8.4
module load R/4.1.1
```

</p>
</details>

## Semaine 1: Vue d'ensemble d'EMOD
Cette semaine, nous discuterons de la structure générale et du contenu d'EMOD et nous nous assurerons que vous êtes prêts à exécuter le modèle sur notre HPC linux, QUEST. Vous allez mettre en place votre propre environnement virtuel pour exécuter EMOD via emodpy et idmtools et cloner ce dépôt github dans votre répertoire personnel sur QUEST. Veuillez vous familiariser avec le dépôt, le site web et la documentation EMOD avant d'exécuter l'exemple simple à la fin de cette semaine.

**Ce à quoi on peut s'attendre**

Cliquez sur la flèche pour développer :
<details><summary><span><em>Exécuter EMOD à partir du terminal</em></span></summary>
<p>

Lorsque vous exécutez un script de simulation EMOD sur QUEST, il génère une série de messages initiaux. Vous verrez un avertissement concernant l'absence de "idmtools.ini" - c'est tout à fait normal car nous n'avons généralement pas besoin du fichier ini pour fonctionner avec emodpy. Après cet avertissement, vous verrez un segment qui vous donne quelques informations de base sur la plateforme idmtools que vous utilisez pour exécuter le script ainsi que le répertoire de travail, où tous les résultats de votre simulation seront stockés.

![](static/example_run.png)

Après une courte période d'attente, vous verrez également des lignes supplémentaires fournissant des informations sur la mise en service de votre/vos simulation(s). Vous pouvez vous attendre à voir une ligne indiquant que la tâche EMODTask est en cours de création, quelques avertissements et avis concernant la création de fichiers, puis les barres indiquant la progression de la découverte des actifs et de la mise en service de la simulation. Une fois la mise en service terminée, vous verrez également l'ID de la tâche QUEST, le répertoire de la tâche, l'ID de la suite et l'ID de l'expérience. Une ligne dans le fichier [run_example.py](https://github.com/numalariamodeling/FE-2023-examples/blob/main/run_example.py) indique au terminal d'attendre que toutes les simulations soient terminées. Il y a donc une barre de progression supplémentaire et l'affirmation que l'expérience a réussi ou échoué (une fois terminée) qui peut ne pas être présente dans toutes les exécutions si cette ligne est exclue. Notez que nous avons commandé et exécuté avec succès une simulation ici (voir 1/1 à la fin des barres de progression).

![](static/example_commission.png)

</p>
</details>

<details><summary><span><em>Structure du fichier</em></span></summary>
<p>

Si vous vous rendez dans le répertoire du travail, la structure du fichier devrait ressembler à celle ci-dessous. Elle peut être résumée comme suit :

- Répertoire des emplois
    - ID de la suite
        - ID de l'expérience
            - Actifs de l'expérience (par exemple, données démographiques, exécutable EMOD, fichiers climatiques, etc.)
            - Identifiant(s) de simulation
                - Dossier de sortie (par exemple, rapporteurs spécifiés dans le script d'exécution)
                - Sorties générales de la simulation (par exemple, fichiers de campagne et de configuration, suivi de l'état/des erreurs, métadonnées de la simulation)
            - Sorties générales de l'expérience (par exemple, suivi de l'état et des erreurs, métadonnées de l'expérience)
        - Fichier de métadonnées de la suite
            
*Note : Tous les dossiers ID sont des chaînes alphanumériques à 16 chiffres générées par idmtools, il n'y a actuellement aucun moyen de les modifier pour utiliser des noms plus lisibles par l'homme.*

![](static/example_file_structure.png)

</p>
</details>

**Exemple**

L'exercice de cette semaine présente la version la plus simple de l'exécution et de l'analyse d'une expérience de simulation unique dans EMOD en utilisant l'infrastructure emodpy/idmtools et python. Avant d'exécuter une simulation, il faut vérifier que toutes les configurations et installations ont été effectuées avec succès et modifier les chemins dans le fichier manifeste. Les étapes sont généralement les suivantes

1. exécuter la simulation, et   
2. analyser les résultats de la simulation 

**Instructions**

Cliquez sur la flèche pour développer :
<details><summary><span><em>Exécuter une simulation EMOD simple</em></span></summary>
<p>

- Naviguez jusqu'à votre copie locale de ce dépôt sur QUEST : `cd ~/FE-2023-examples`  
- Notez le chemin de votre répertoire de travail dans `manifest.py` : `/projects/b1139/FE-2023-examples/experiments/<username>`. Cela vous aidera à suivre vos simulations séparément des autres participants.
- *Note: chaque fois que vous voyez des éléments entre `< >`, ils doivent être remplacés ENTIÈREMENT par ce qui est étiqueté comme étant l'élément en question. Par exemple, si votre nom d'utilisateur est `abc123`, alors ce répertoire de travail sera:* `/projects/b1139/FE-2023-examples/experiments/abc123`
- Chargez votre environnement virtuel emodpy `SLURM_LOCAL` (voir les prérequis)  
- Lancez la simulation via `python3 run_example.py`
- Attendez que la simulation se termine (~2 minutes)  
- Allez dans le répertoire de travail (voir `experiments/<username>` ci-dessus) pour trouver l'expérience générée - elle sera sous un ensemble de chaînes alphanumériques de 16 chiffres. La structure de ces chaînes est `Suite > Expérience > Simulations`. En raison des systèmes de gestion actuels de SLURM, vous ne pourrez pas voir le nom de l'expérience donné dans le script `run_example.py`; cependant, il peut être trouvé dans les fichiers metadata.json au niveau de l'expérience et de la simulation. Vous pouvez également choisir de trier vos fichiers en fonction du temps, de sorte que les expériences les plus récentes apparaissent en premier. 
- Jetez un coup d'œil à ce qui a été généré même lors de cette simple exécution et familiarisez-vous avec la structure des fichiers. Vous devez toujours vérifier vos résultats après avoir effectué des simulations pour vous assurer qu'ils correspondent à ce que vous attendiez. 
- *Note: assurez-vous d'aller jusqu'au bout de la structure des dossiers pour voir vos simulations et leurs résultats. Pour plus d'informations sur ce à quoi vous pouvez vous attendre, voir [Semaine 1 "Ce à quoi on peut s'attendre"](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.fr.md#semaine-1--vue-densemble-demod).*

</p>
</details>

## Semaine 2: Les éléments de base

Le premier exercice de cette semaine montre comment créer des fichiers d'entrée, tels que des fichiers démographiques et climatiques, et comment les incorporer dans la simulation. L'exercice explique également comment modifier les paramètres de configuration (par exemple, la taille de la population ou la durée de la simulation).

Le deuxième exercice de cette semaine se concentre sur l'ajout de rapporteurs et l'observation des changements dans les résultats de simulation basés sur les sorties des modèles `InsetChart.json` et `MalariaSummaryReport.json`.

**Instructions**

Cliquez sur la flèche pour développer :
<details><summary><span><em>Ajouter des entrées</em></span></summary>
<p>

Cet exercice montre comment créer des fichiers démographiques et climatiques et comment les incorporer dans la simulation. Il montre également comment modifier les paramètres de configuration (par exemple, le nombre d'exécutions ou la durée de la simulation). Effectuez toutes les étapes ci-dessous avant d'exécuter l'exemple suivant.


1. Extraire les données climatiques et les ajouter aux simulations
    - Consultez le fichier `example_site.csv` dans le [dossier inputs](https://github.com/numalariamodeling/FE-2023-examples/tree/main/inputs). Ce fichier contient les coordonnées d'un site d'exemple en Ouganda et établit que ce site sera notre "Node 1" dans le modèle. Vous pouvez utiliser ces coordonnées ou sélectionner un site différent (et ajuster les coordonnées en conséquence) si vous le souhaitez pour le reste de cet exemple.
    - Ensuite, nous allons lancer `extract_weather.py` - ce script va lancer le générateur de météo. Notez qu'il lit les informations de `example_site.csv` pour trouver le bon site et vous pouvez demander la météo pour la période qui vous intéresse. Vous verrez également que la plateforme utilisée s'appelle *Calculon* - il s'agit du HPC de l'IDM _(nécessite un accès à la base de données climatiques : demandez à quelqu'un de l'équipe NU)_.
        - Nous pouvons également lancer `recreate_weather.py` qui convertira les fichiers météo que nous venons de générer dans un format csv que nous pourrons modifier. Pour cet exemple, nous n'avons pas besoin de faire de modifications, mais cela peut être utile pour des questions de recherche telles que celles liées au changement climatique. Après avoir effectué toutes les modifications dans le script, nous reconvertissons les csv en fichiers météorologiques.  
    - Maintenant que vous savez ce que font les scripts, chargez votre environnement virtuel et utilisez `python3 extract_weather.py` pour lancer l'extraction.   
        - Entrez vos identifiants pour accéder à Calculon et attendez que vos fichiers météo soient générés. Lorsque c'est terminé, vérifiez les entrées de votre repo pour vous assurer que les fichiers ont bien été créés.   
        - Lancez ensuite `python3 recreate_weather.py` et vérifiez que les fichiers météo modifiés ont été créés. Assurez-vous de vérifier le script `recreate_weather.py` pour voir où ils doivent être situés.
    - Copiez `run_example.py` et nommez le `run_example_inputs.py` et dans le script changez le nom de l'expérience en `f'{user}_FE_example_inputs'`
    - Mettez à jour les paramètres par défaut dans votre script de simulation (`run_example_inputs.py`)'s `set_param_fn()`. Vous aurez aussi besoin d'ajouter votre dossier de fichiers climatiques comme répertoire d'actifs à la tâche EMODTask dans `general_sim()`, cela doit être fait après que la tâche soit définie et avant que l'expérience ne soit créée. Il est recommandé de placer ce répertoire après le "set sif":

    ```python
    def set_param_fn():
        ## contenu existant
        config.parameters.Air_Temperature_Filename = os.path.join('climate',
            'example_air_temperature_daily.bin')
        config.parameters.Land_Temperature_Filename = os.path.join('climate',
            'example_air_temperature_daily.bin')
        config.parameters.Rainfall_Filename = os.path.join('climate',
            'example_rainfall_daily.bin')
        config.parameters.Relative_Humidity_Filename = os.path.join('climate', 
            'example_relative_humidity_daily.bin')

    ```
    ```python
    def general_sim():   
        ## contenu existant
        task.set_sif(manifest.SIF_PATH, platform)
    
        # ajouter le répertoire météorologique comme atout
        task.common_assets.add_directory(os.path.join(manifest.input_dir,
            "example_weather", "out"), relative_path="climate")
    ```

2. Ajouter des données démographiques
    - Vous avez peut-être remarqué la fonction `build_demog()` dans le premier exemple, nous allons maintenant l'examiner plus en détail. Il y a plusieurs façons d'ajouter des détails démographiques à nos simulations, principalement avec un nouveau générateur où nous ajoutons des détails au fur et à mesure ou à partir d'un csv ou nous pouvons lire un fichier json pré-fait. Ici, nous allons utiliser la commande `from_template_node` dans emodpy_malaria demographics avec quelques informations de base, comme la latitude et la longitude. Nous devons importer cette fonctionnalité directement depuis emodpy_malaria - vous devriez le voir en haut de votre script
    - Dans la fonction `build_demog()`, vous devriez voir la commande template node, ajouter la latitude et la longitude pour votre site d'exemple et augmenter la taille de l'échantillon à 1000.
    - Nous voulons également ajouter la dynamique vitale d'équilibre à notre script. Cela permettra d'égaliser les taux de natalité et de mortalité afin d'obtenir une population relativement stable dans nos simulations. Pour certaines expériences, il peut être souhaitable de définir ces taux séparément, mais pour l'instant, cette version simple répondra à nos besoins. Ajoutez `SetEquilibriumVitalDynamics()` directement au fichier de démographie que nous créons dans la fonction de génération (comme on le voit ci-dessous).
    - Il existe de nombreux aspects de la démographie que nous pouvons spécifier, tels que la dynamique vitale mentionnée précédemment, les distributions de risque et les distributions d'âge. L'emod_api contient des distributions d'âge existantes. Nous allons devoir importer ces PreDefined Distributions et les ajouter avec `SetAgeDistribution` à notre fichier de démographie. Essayons d'ajouter la distribution générale pour l'Afrique sub-saharienne.
    
    ```python
    import emodpy_malaria.demographics.MalariaDemographics as Demographics
    import emod_api.demographics.PreDefinedDistributions as Distributions

    def build_demog():
        """
        Cette fonction construit un fichier d'entrée démographique pour le DTK en utilisant emod_api.
        """

        demog = Demographics.from_template_node(lat=0.4479, lon=33.2026,
                                                pop=1000, name="Example_Site")
        demog.SetEquilibriumVitalDynamics()
    
        age_distribution = Distributions.AgeDistribution_SSAfrica
        demog.SetAgeDistribution(age_distribution)

        return demog
    ```

3. Modification des paramètres de configuration
    - Nous voulons aussi souvent modifier certains des [paramètres de configuration](https://docs.idmod.org/projects/emod-malaria/en/latest/parameter-configuration.html) qui contrôlent des choses comme le modèle intra-hôte, les vecteurs et la configuration de la simulation. Dans `run_example.py`, nous définissons les valeurs par défaut de l'équipe paludisme en utilisant `config = conf.set_team_defaults(config, manifest)`, mais nous pouvons également spécifier des paramètres individuels comme nous l'avons fait avec les noms des fichiers climatiques. Commençons par des choses simples comme l'ajout du réglage de la `Simulation_Duration` (la durée de la simulation en jours) et du `Run_Number` (la graine aléatoire pour la simulation) dans `set_param_fn()`. Ces deux paramètres peuvent être utilisés directement en les référençant comme `config.parameters.<param_name>` et en les réglant à la valeur désirée. L'équipe utilise généralement une structure de `sim_years*365` avec sim_years défini globalement, en haut du script sous toutes les importations, pour définir la durée.
    - Fixez la durée à 1 an et le numéro d'exécution à n'importe quel nombre de votre choix
        - *Note: cette valeur est juste la valeur de la graine aléatoire, PAS le nombre de réalisations stochastiques à exécuter.*
    - Ensuite, nous allons ajouter quelques espèces de moustiques. Il existe une fonction spécifique pour cela, `add_species()` dans emodpy_malaria malaria config. Essayez d'ajouter *A. gambiae*, *A. arabiensis*, et *A. funestus* à votre fichier de configuration:
            
    ```python    
    sim_years = 1

    def set_param_fn():
        ## existing contents
    
        conf.add_species(config, manifest, ["gambiae", "arabiensis", "funestus"])

        config.parameters.Simulation_Duration = sim_years*365
        config.parameters.Run_Number = 0
    ```

4. Maintenant que vous avez ajouté ces changements, essayez d'exécuter votre nouveau script avec `python3 run_example_inputs.py`. Une fois qu'il a réussi, allez vérifier ce qui s'est exécuté. Voyez-vous les changements dans votre demographics.json et le dossier climate dans le répertoire `Assets` de l'expérience ? Et dans config.json ou stdout.txt ? Vous devriez également voir [`InsetChart.json`](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-inset-chart.html) dans le dossier output de la simulation - il s'agit du rapport par défaut d'EMOD qui vous donnera une idée de ce qui se passe dans votre simulation. Nous étudierons ce rapport plus en détail dans la section Analyse de la Semaine 2.

</p>
</details>


<details><summary><span><em>Ajouter des sorties</em></span></summary>
<p>

Cet exercice montre comment ajouter à nos simulations certains des rapports intégrés sur le paludisme. Ces rapports peuvent nous aider à comprendre ce qui se passe dans nos simulations, qu'il s'agisse d'objectifs de base tels que l'incidence et la prévalence ou d'images plus détaillées d'événements ou de données internes à l'hôte telles que la parasitémie. Vous pouvez en savoir plus sur les types d'analyseurs possibles dans la [documentation du fichier de sortie EMOD](https://docs.idmod.org/projects/emod-malaria/en/latest/software-outputs.html). Dans cet exercice, nous allons ajouter l'enregistreur de rapport d'événement et le rapport de synthèse sur le paludisme aux simulations.

- Copiez votre script `run_example_inputs.py` et nommez-le `run_example_outputs.py`. Changez le nom de l'expérience en `f'{user}_FE_example_outputs'`.
- Nous devons importer les reporters de la malaria depuis emodpy_malaria. Vous devrez ajouter cette ligne au reste de vos importateurs emodpy_malaria `from emodpy_malaria.reporters.builtin import *` au début de votre script. Remarquez le "*" à la fin, cela signifie que nous importons tous les reporters du script de reporter intégré par leurs noms.
- [Report Event Recorder](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-event-recorder.html) nous permet de voir les différents événements qui se produisent pour chaque individu dans notre sim, ainsi que des informations démographiques et de santé de base sur l'individu. Ce rapport est particulièrement utile pour le suivi de différentes interventions, telles que l'administration d'un traitement, mais pour l'instant, nous nous contenterons d'examiner des événements simples tels que les naissances ou les anniversaires d'individus existants. Nous pouvons contrôler la période sur laquelle nous voulons établir le rapport, de `start_day` à `end_day`, ainsi que des éléments tels que le groupe d'âge cible et les nœuds pendant que nous ajoutons le rapporteur. Pour l'instant, ajoutons le rapport pour l'ensemble de la simulation et en ciblant les âges de 0 à 100 ans, donc probablement toute la population. Il peut être ajouté à notre `general_sim()` avec `add_event_recorder()` après que la tâche ait été définie, autour de la ligne 110:
    ```python
    def general_sim()
        ## existing contents
    
        add_event_recorder(task, event_list=["HappyBirthday", "Births"],
                           start_day=1, end_day=sim_years*365, 
                           node_ids=[1], min_age_years=0,
                           max_age_years=100)
    ```

- Le [Malaria Summary Report](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-malaria-summary.html) fournit un résumé des données sur le paludisme au niveau de la population, regroupées en différentes catégories telles que l'âge, la parasitémie et l'infectiosité. Ce rapport nous fournira des informations telles que la PPR, l'incidence clinique et la population stratifiée dans le temps (ainsi que les tranches d'âge, la parasitémie et l'infectiosité si vous le souhaitez). Nous pouvons spécifier la période d'agrégation qui nous intéresse, typiquement hebdomadaire, mensuelle ou annuelle par le biais de l'intervalle de rapport. La documentation liée vous montrera beaucoup d'autres choses que nous pouvons spécifier aussi, mais pour l'instant nous allons garder les choses simples et définir notre rapport à exécuter mensuellement pour la durée de la simulation avec des groupes d'âge simples : 0-0.25, 0.25-5, et 5-115 ans. Nous allons également indiquer au rapport que nous voulons un maximum de 20 intervalles afin d'être sûrs d'obtenir tous nos rapports mensuels pour 1 an et utiliser `pretty_format` pour rendre le rapport de sortie plus lisible pour nous. Vous devez également ajouter un suffixe au nom de fichier, dans ce cas nous utiliserons "monthly" pour donner une description supplémentaire au rapport. Ceci doit être ajouté directement après le Report Event Recorder, également dans `general_sim()` avec `add_malaria_summary_report()`:
    ```python
    def general_sim()
        ## contenu existant
    
        ## enregistreur d'événements ajouté précédemment
    
        add_malaria_summary_report(task, manifest, start_day=1, 
                                   end_day=sim_years*365, 
                                   reporting_interval=30,
                                   age_bins=[0.25, 5, 115],
                                   max_number_reports=20,
                                   filename_suffix='monthly',
                                   pretty_format=True)
    ```

- Essayez d'exécuter votre nouveau script comme vous l'avez appris dans les deux derniers exemples et attendez qu'il se termine avant de naviguer vers votre répertoire d'expériences. Une fois l'exécution terminée, vérifiez les résultats de la simulation et votre nouveau rapport. Vérifiez que les fichiers ont bien été créés et regardez ce qu'ils contiennent. Que remarquez-vous ?
    - *Conseil: il est particulièrement important de vérifier tous vos résultats lorsque vous apportez des modifications importantes à votre script. Si vous ne les examinez pas, vous risquez de passer à côté de problèmes qui ne sont pas à l'origine de l'échec de vos simulations (mais qui font quelque chose que vous ne voulez pas qu'ils fassent).*

</p>
</details>
