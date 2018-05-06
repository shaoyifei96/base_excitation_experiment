This describes the method of using the VideoProcessor.py script to determine the displacement transmissibility of a system using ArUcO stickers.

To begin, using a calibrated camera (calibration instructions can be found in the folder "calibration") record a video of the stickers moving for one setting of damping,
weight, spring constant, etc. for each of the frequencies that you wish to take data for. Once the data has been collected, rename the videos with the following convention:

camera_w_m_c_k_n.mp4

where:
w is the value of the rate of excitation.
m is the weight of the mass on the end of the spring.
c is the damping setting on the damper.
k is the spring constant that you used.
n is the trail number with these settings (if there are mulitple).

Once the videos are named correctly move them into the input folder. Ensure that only the data with this trial is in the folder (so the file names should be identical except 
for the variable being changed between videos). If there already were videos in the input folder, be sure to move them or delete them otherwise the code will process them too.

Once these steps have been completed run the script. It should output the data for the displacement transmissibility function into graphs and videos in the output folder. 