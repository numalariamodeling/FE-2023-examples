# FE-2023-examples
Exemples de scripts pour le programme 2023 d'enrichissement de la faculté en modélisation appliquée du paludisme à Northwestern.

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.md)
[![fr](https://img.shields.io/badge/lang-fr-red.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.fr.md)

## Voie technique (EMOD)

**Vue d'ensemble** : 
Les exercices consistent généralement en une simulation et un analyseur des sorties de simulation. 
Certaines semaines, des scripts supplémentaires existent pour préparer les entrées de la simulation ou générer des sorties et des graphiques supplémentaires, ou encore pour la calibration du modèle, comme décrit dans les instructions des semaines respectives.

**Vérification des résultats:**
Pour chaque semaine, des suggestions de scripts de simulation pour la comparaison ou l'aide pendant l'exercice sont fournies dans le dossier de la semaine respective.

**Conditions préalables** : 
Avant d'exécuter les scripts d'exemple hebdomadaires, veuillez vous assurer qu'emodpy a été [installé] ((https://faculty-enrich-2022.netlify.app/modules/install-emod/))
et que le [référentiel a été cloné](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
dans votre répertoire personnel sur quest, idéalement sous la forme _/home/<.username>/FE-23-examples_.
L'exécution de vos scripts nécessitera que l'environnement virtuel emodpy soit chargé et suppose que les fichiers soient exécutés depuis un répertoire de travail défini à l'endroit où se trouve le script. Avant de commencer un exercice, assurez-vous que vous avez extrait ou récupéré les dernières modifications du dépôt (voir git-guides [git-pull](https://github.com/git-guides/git-pull)).

### Semaine 1 : Vue d'ensemble d'EMOD
Cette semaine, nous discuterons de la structure générale et du contenu d'EMOD et nous nous assurerons que vous êtes prêts à exécuter le modèle sur notre HPC basé sur linux, QUEST. Vous allez configurer votre propre environnement virtuel pour exécuter EMOD via emodpy et idmtools et cloner ce dépôt github dans votre répertoire personnel sur QUEST. Nous n'exécuterons pas de scripts d'exemple, mais nous vous invitons à vous familiariser avec le dépôt, le site web et la documentation EMOD.

### Semaine 2 : Blocs de construction
Le premier exercice de cette semaine présente la version la plus simple pour exécuter et analyser une seule expérience de simulation dans EMOD en utilisant l'infrastructure emodpy/idmtools et python. Avant de lancer une simulation, il faut vérifier que toutes les configurations et installations se sont déroulées avec succès et modifier les chemins dans le fichier manifeste. Les étapes consistent généralement à 1) exécuter la simulation et 2) analyser les résultats de la simulation. 

Le deuxième exercice de cette semaine montre comment créer des fichiers démographiques et climatiques et comment les intégrer dans la simulation. L'exercice présente également comment modifier les paramètres de configuration (c'est-à-dire la taille de la population ou la durée de la simulation).

L'exercice final de cette semaine se concentrera sur l'observation des changements dans les résultats de simulation basés sur les sorties de modèle InsetChart.json et MalariaSummaryReport.json.
