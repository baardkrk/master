
Skeleton Extraction with Convolutional Neural Networks
======================================================

Ekstrahere mennesklig posering/skjelett fra dybdebilder med CNNs.


Fremdriftsplan 2020
-------------------

**Skriving av oppgave:**
 - [ ] Abstrakt [#-------------------] (5%)
 - [ ] Introduksjon [#####---------------] (25%)
 - [ ] Bakgrunnskapittel [#-------------------] (5%)
 - [ ] Metode [##------------------] (10%)
 - [ ] Eksperimenter [--------------------] (0%)
 - [ ] Konklusjoner [--------------------] (0%)
 - [ ] Future work [--------------------] (0%)
 
 **Delmål:**
 - [x] Få styring på bakgrunnsmateriale
 - [ ] Laste ned datasett *(1 uke)*
   - [x] MHAD
   - [ ] Human 3.6m
   - [ ] Panoptic Studio
 - [ ] Oversette datasett til trenbart format *(2 uker)*
   | MHAD | Human 3.6m | Panoptic Studio | Oppgave                                                           |
   |:----:|:----------:|:---------------:| ----------------------------------------------------------------- |
   | [ ]  |    [ ]     |       [ ]       | Pare opp ground-truth landemerker med dybdebilder                 |
   | [ ]  |    [ ]     |       [ ]       | Flytte origo av hvert koordinatsystem til kameraets senter        |
   | [ ]  |    [ ]     |       [ ]       | Rotasjon av input -- det er *formen* på mennesker vi er ute etter |
 - [ ] Plukke ut treningsverdier fra datasettene *(1 uke)*
   - [ ] Dele opp i trening/validering/testsett
   - [ ] Muligens lage et testsett som ikke har roterte data
 - [ ] Skrive arkitektur for ML algoritme (kraftig GPU) *(4 uker)*
   - [ ] Sette seg inn i utviklingsverktøy (PyTorch, Tensorflow, ..)
   - [ ] Sette opp arkitektur
   - [ ] Optimere for vanlige ML feil (vanishing gradient++)
 - [ ] Sette opp arbeidsområde på skolens GPU-maskin *(.5 uke)*
 - [ ] Trene modell på GPU-maskin *(2 uker)*
 - [ ] Vurdere resultater fra testsett *(1 uke)*
 - [ ] Skrive om arkitektur *(2 uker)*
 - [ ] Optimering av forward-algoritme for portabel HW *(1 uke)*
 - [ ] Implementasjon på portabel hardware *(1.5 uke)*
 - [ ] Test av algoritme på protabel HW *(.5 uke)*
 
**Dersom tid:**
 - [ ] Lage noen enkle treningssett med aktivitetsgjenkjenning
 - [ ] Skrive algoritme for aktivitetsgjennkjenning av noen utvalgte aktiviteter
 - [ ] Teste på portabel HW

*Totalt allokert tid: 16.5 uker*

