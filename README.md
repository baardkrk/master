
Skeleton Extraction with Convolutional Neural Networks
======================================================

Ekstrahere mennesklig posering/skjelett fra dybdebilder med CNNs.


Fremdriftsplan 2020
-------------------

**Delmål:**
 - [x] Laste ned datasett *(1 uke)*
 - [ ] Oversette datasett til trenbart format *(2 uker)*
   - Pare opp ground-truth landemerker med dybdebilder
   - Flytte origo av hvert koordinatsystem til kameraets senter
   - Rotasjon av input -- det er *formen* på mennesker vi er ute etter
 - [ ] Plukke ut treningsverdier fra datasettene *(1 uke)*
   - Dele opp i trening/validering/testsett
   - Muligens lage et testsett som ikke har roterte data
 - [ ] Skrive arkitektur for ML algoritme (kraftig GPU) *(4 uker)*
   - Sette seg inn i utviklingsverktøy (PyTorch, Tensorflow, ..)
   - Sette opp arkitektur
   - Optimere for vanlige ML feil (vanishing gradient++)
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

*Totalt allokert tid: 16 uker*
