MHAD explanation
================

Kinect Hierarchy:
Kinect -> Subject -> Action -> Repetition

It's the same hierarchy when naming files. So, for correspondence
files we have the naming convention `corr_moc_kin01_s04_a02_r02.txt` 
containing the correspondences of `kinect 01` `subject 04` `action 02` 
`repetition 02`

In the dataset we have two kinects, observing the subject from two sides.
We have a total of 10 subjects, 11 actions, doing 5 repetitions each.  
The actions are:

| Action | Repetitions | Recordings | \~Length/recording | Samples |
|:------ |:-----------:|:----------:|:-------- | ------:|
| Jumping in place | 5 | 5 | 5 sec | 10x5x5 |
| Jumping jacks | 5 | 5 | 7 sec | 10x5x7 |
| Bending -- hands up all the way down | 5 | 5 | 12 sec | 10x5x12 |
| Punching (boxing) | 5 | 5 | 10 sec | 10x5x10 |
| Waving -- two hands | 5 | 5 | 7 sec | 10x5x7 |
| Waving -- one hand (right) | 5 | 5 | 7 sec | 10x5x7 |
| Clapping hands | 5 | 5 | 5 sec | 10x5x5 |
| Throwing a ball | 1 | 5 | 3 sec | 10x5x3 |
| Sit down then stand up | 5 | 5 | 15 sec | 10x5x15 |
| Sit down | 1 | 5 | 2 sec | 10x5x2 |
| Stand up | 1 | 5 | 2 sec | 10x5x2 |

if we assume what we want to get is human bodies in different positions, 
we can assume that we can get a sample every 1 seconds. That gives us 
a total of 3750 usable samples.
Hardly enough to train on...

In each correspondence file we have the first number reffering to the 
kinect frame.
