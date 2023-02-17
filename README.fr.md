# FE-2023-examples
Exemples de scripts pour le programme 2023 d'enrichissement de la faculté en modélisation appliquée du paludisme à Northwestern.

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.md)
[![fr](https://img.shields.io/badge/lang-fr-red.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.fr.md)

## Voie technique (EMOD)

**Vue d'ensemble:** 
Les exercices consistent généralement en une simulation et un analyseur des sorties de simulation. 
Certaines semaines, des scripts supplémentaires existent pour préparer les entrées de la simulation ou générer des sorties et des graphiques supplémentaires, ou encore pour la calibration du modèle, comme décrit dans les instructions des semaines respectives.

**Vérification des résultats:**
Pour chaque semaine, des suggestions de scripts de simulation pour la comparaison ou l'aide pendant l'exercice sont fournies dans le dossier de la semaine respective.

**Conditions préalables:**  
Avant d'exécuter les scripts d'exemple hebdomadaires, veuillez vous assurer qu'emodpy a été [installé](https://faculty-enrich-2022.netlify.app/modules/install-emod/)
et que le [référentiel a été cloné](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
dans votre répertoire personnel sur quest, idéalement sous la forme _/home/<.username>/FE-2023-examples_.
L'exécution de vos scripts nécessitera que l'environnement virtuel emodpy soit chargé et suppose que les fichiers soient exécutés depuis un répertoire de travail défini à l'endroit où se trouve le script. Avant de commencer un exercice, assurez-vous que vous avez extrait ou récupéré les dernières modifications du dépôt (voir git-guides [git-pull](https://github.com/git-guides/git-pull)).

### Semaine 1: Vue d'ensemble d'EMOD
Cette semaine, nous discuterons de la structure générale et du contenu d'EMOD et nous nous assurerons que vous êtes prêts à exécuter le modèle sur notre HPC basé sur linux, QUEST. Vous allez configurer votre propre environnement virtuel pour exécuter EMOD via emodpy et idmtools et cloner ce dépôt github dans votre répertoire personnel sur QUEST. Nous n'exécuterons pas de scripts d'exemple, mais nous vous invitons à vous familiariser avec le dépôt, le site web et la documentation EMOD.

### Semaine 2: Blocs de construction
Le premier exercice de cette semaine présente la version la plus simple pour exécuter et analyser une seule expérience de simulation dans EMOD en utilisant l'infrastructure emodpy/idmtools et python. Avant de lancer une simulation, il faut vérifier que toutes les configurations et installations se sont déroulées avec succès et modifier les chemins dans le fichier manifeste. Les étapes consistent généralement à 1) exécuter la simulation et 2) analyser les résultats de la simulation. 

Le deuxième exercice de cette semaine montre comment créer des fichiers démographiques et climatiques et comment les intégrer dans la simulation. L'exercice présente également comment modifier les paramètres de configuration (c'est-à-dire la taille de la population ou la durée de la simulation).

L'exercice final de cette semaine se concentrera sur l'observation des changements dans les résultats de simulation basés sur les sorties de modèle InsetChart.json et MalariaSummaryReport.json.

**Instructions**

Cliquez sur la flèche pour développer:
<details><summary><span><em>Exécuter une simulation EMOD simple</em></span></summary>
<p>

- Naviguez vers votre copie locale de ce dépôt sur QUEST: `cd ~/FE-2023-examples`.
- Ajustez les chemins dans `manifest.py` en ajoutant votre nom d'utilisateur/netID à la fin du répertoire de travail: `/projects/b1139/FE-2023-examples/experiments/<username>`. This will help your track your simulations separately from other participants.
- Chargez votre environnement virtuel emodpy `SLURM_LOCAL`.
- Lancez la simulation avec `python3 example_run.py -l`.
- Attendez la fin de la simulation (~2 minutes)
- Allez dans le dossier `expériences/<votre nom d'utilisateur>` pour trouver l'expérience générée - elle sera sous un ensemble de chaînes alphanumériques à 16 chiffres. La structure de ces chaînes est `Suite > Experiment > Simulations`. En raison des systèmes de gestion actuels de SLURM, vous ne serez pas en mesure de voir le nom de l'expérience donné dans le script `example_run.py`; cependant, il peut être trouvé dans les fichiers metadata.json de niveau expérience et simulation. Vous pouvez également choisir de trier vos fichiers en fonction du temps, de sorte que les expériences les plus récentes apparaissent en premier. Jetez un coup d'œil à ce qui a été généré même dans cette simple exécution.

</p>
</details>

<details><summary><span><em>Ajouter des entrées</em></span></summary>
<p>

Cet exercice montre comment créer des fichiers démographiques et climatiques et comment les intégrer dans la simulation. Il présente également comment modifier les paramètres de configuration (par exemple, le nombre d'exécutions ou la durée de la simulation). Effectuez toutes les étapes ci-dessous avant d'exécuter l'exemple suivant.



1. Extraction des données climatiques et ajout aux simulations
    - Regardez le fichier `example_site.csv` dans le [dossier inputs] (https://github.com/numalariamodeling/FE-2023-examples/tree/main/inputs). Ce fichier contient les coordonnées d'un site d'exemple en Ouganda et établit que ce sera notre "Nœud 1" dans le modèle. Vous pouvez utiliser ces coordonnées ou sélectionner un site différent (et ajuster les coordonnées en conséquence) si vous le souhaitez pour le reste de cet exemple.
    - Ensuite, nous allons exécuter `extract_weather.py` - ce script va lancer le générateur de météo. Remarquez qu'il lit les informations de `example_site.csv` pour chercher le bon site et vous pouvez demander la météo pour la période qui vous intéresse. Vous verrez aussi que la plateforme pour cela s'appelle *Calculon* - c'est le HPC de l'IDM _(nécessite un accès à la base de données climatiques: demandez à quelqu'un de l'équipe NU)_.
    - Nous pouvons aussi lancer `recreate_weather.py` qui convertira les fichiers météo que nous venons de générer en un format csv que nous pourrons modifier. Pour cet exemple, nous n'avons pas besoin de faire de modifications mais cela peut être utile pour des questions de recherche telles que celles relatives au changement climatique. Après avoir effectué toutes les modifications dans le script, nous reconvertissons le csv en fichiers météo.
    - Maintenant que vous savez ce que font les scripts, chargez votre environnement virtuel et utilisez `python3 extract_weather.py` pour lancer l'extraction. Entrez les informations d'identification pour accéder à Calculon et attendez que vos fichiers météo soient générés, quand c'est terminé, vérifiez les entrées de votre dépôt pour vous assurer que les fichiers sont là. Lancez ensuite `python3 recreate_weather.py` et vérifiez que les fichiers météo modifiés ont été créés. Assurez-vous de vérifier le script `recreate_weather.py` pour voir où ils doivent être situés.
    - Copiez `example_run.py` et nommez-le `example_run_inputs.py` et dans le script changez le nom de l'expérience en `f'{user}_FE_example_inputs'`.
    - Mettez à jour les paramètres par défaut dans la fonction `set_param_fn()` de votre script de simulation (`example_run_inputs.py`). Vous devrez également ajouter votre dossier de fichiers climatiques en tant que répertoire d'actifs à la tâche EMODTask dans general_sim(), ceci doit être défini après que la tâche soit définie et avant que l'expérience soit créée. Il est recommandé de mettre ce répertoire après le "set sif":
   
```py
def set_param_fn():
    ## existing contents
    config.parameters.Air_Temperature_Filename = os.path.join('climate','example_air_temperature_daily.bin')
    config.parameters.Land_Temperature_Filename = os.path.join('climate','example_air_temperature_daily.bin')
    config.parameters.Rainfall_Filename = os.path.join('climate','example_rainfall_daily.bin')
    config.parameters.Relative_Humidity_Filename = os.path.join('climate', 'example_relative_humidity_daily.bin')

```
    
```py
def general_sim():   
    ## existing contents
    task.set_sif(manifest.SIF_PATH, platform)
    
    # add weather directory as an asset
    task.common_assets.add_directory(os.path.join(manifest.input_dir, "example_weather", "out"), relative_path="climate")
```

2. Ajouter des données démographiques
    - Vous avez peut-être remarqué la fonction `build_demog()` dans le premier exemple, nous allons maintenant l'examiner plus en détail. Il y a plusieurs façons d'ajouter des détails démographiques à nos simulations, principalement avec un nouveau générateur où nous ajoutons des détails au fur et à mesure ou à partir d'un csv ou nous pouvons lire dans un fichier json pré-fait. Ici, nous allons utiliser la commande `from_template_node` dans emodpy_malaria demographics avec quelques informations de base, comme la latitude et la longitude. Nous devons importer cette fonctionnalité directement depuis emodpy_malaria - vous devriez voir ceci en haut de votre script
    - Dans la fonction `build_demog()`, vous devriez voir la commande template node, ajouter la latitude et la longitude pour votre site d'exemple et augmenter la taille de l'échantillon à 1000.
    - Nous voulons également ajouter la dynamique vitale d'équilibre à notre script. Cela permettra d'égaliser les taux de naissance et de mortalité afin d'avoir une population relativement stable dans nos simulations. Pour certaines expériences, il peut être souhaitable de les définir séparément, mais pour l'instant, cette version simple répondra à nos besoins. Ajoutez `SetEquilibriumVitalDynamics()` directement au fichier de démographie que nous créons dans la fonction générateur (comme vu ci-dessous).
    - Il existe de nombreux aspects de la démographie que nous pouvons spécifier, tels que la dynamique vitale mentionnée précédemment, les distributions de risque et les distributions d'âge. L'emod_api contient des distributions d'âge existantes. Nous devrons importer ces distributions prédéfinies, puis les ajouter avec `SetAgeDistribution` à notre fichier démographique. Essayons d'ajouter la distribution générale pour l'Afrique sub-saharienne.
    
```py
import emodpy_malaria.demographics.MalariaDemographics as Demographics
import emod_api.demographics.PreDefinedDistributions as Distributions

def build_demog():
    """
    This function builds a demographics input file for the DTK using emod_api.
    """

    demog = Demographics.from_template_node(lat=0.4479, lon=33.2026, pop=1000, name="Example_Site")
    demog.SetEquilibriumVitalDynamics()
    
    age_distribution = Distributions.AgeDistribution_SSAfrica
    demog.SetAgeDistribution(age_distribution)

    return demog
```

3. Modification des configurations
    - Nous voulons aussi souvent modifier certains des [paramètres de configuration](https://docs.idmod.org/projects/emod-malaria/en/latest/parameter-configuration.html) qui contrôlent des choses comme le modèle intra-hôte, les vecteurs, et la configuration de la simulation. Dans `example_run.py`, nous définissons les paramètres par défaut de l'équipe paludisme en utilisant `config = conf.set_team_defaults(config, manifest)`, mais nous pouvons aussi spécifier des paramètres individuels comme nous l'avons fait avec les noms des fichiers climatiques. Commençons par des choses simples comme ajouter le réglage de la `Simulation_Duration` (combien de temps la simulation doit se dérouler en jours) et le `Run_Number` (la graine aléatoire pour la simulation) dans `set_param_fn()`. On peut faire ces deux choses directement en les référençant comme `config.parameters.<param_name>` et en les rendant égaux à la valeur désirée. L'équipe utilise généralement une structure de `sim_years*365` avec sim_years défini globalement, en haut du script sous toutes les importations, pour définir la durée.
    - Définissez la durée à 1 an et le numéro d'exécution à n'importe quel nombre de votre choix.
    - Ensuite, nous allons ajouter quelques espèces de moustiques. Il y a une fonction spécifique pour cela, `add_species()` dans la configuration de emodpy_malaria malaria config. Essayez d'ajouter *A. gambiae*, *A. arabiensis*, et *A. funestus* à votre fichier de configuration:
    
```py    
sim_years = 1

def set_param_fn():
    ## existing contents
    
    conf.add_species(config, manifest, ["gambiae", "arabiensis", "funestus"])

    config.parameters.Simulation_Duration = sim_years*365
    config.parameters.Run_Number = 5
```

4. Maintenant que vous avez ajouté ces changements, essayez de lancer votre nouveau script avec `python3 example_run_input.py -l`. Une fois qu'il a réussi, allez vérifier ce qui a été exécuté. Voyez-vous les modifications apportées à votre demographics.json et au dossier climate dans le répertoire `Assets` de l'expérience? Et dans le fichier config.json ou stdout.txt? Vous devriez également voir [`InsetChart.json`](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-inset-chart.html) dans le dossier de sortie de la simulation - c'est le rapport par défaut d'EMOD qui vous donnera une idée de ce qui se passe dans votre simulation. Nous explorerons ce sujet plus tard dans la section Analyse de la Semaine 2.

</p>
</details>


<details><summary><span><em>Ajout de sorties</em></span></summary>
<p>


</p>
</details>

### Semaine 3: Configuration et réglage fin des expériences

**Instructions**
Cliquez sur la flèche pour développer:
<details><summary><span><em>Click to expand</em></span></summary>
<p>

</p>
</details>

### Semaine 4: Répondre aux questions de recherche

**Instructions**
Cliquez sur la flèche pour développer:
<details><summary><span><em>Click to expand</em></span></summary>
<p

</p>
</details>
