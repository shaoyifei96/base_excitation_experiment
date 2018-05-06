This describes the method of using the VideoProcessor.py script to determine the displacement transmissibility of a system using ArUcO stickers.

To begin, make sure that all the required peripheral libraries are installed (located in Requirements.txt).

Once that is completed, using a calibrated camera (calibration instructions can be found in the folder "calibration") record a video of the stickers moving for one setting of damping, weight, spring constant, etc. for each of the frequencies that you wish to take data for. Make sure the video is about 20-30 seconds long or long enough to see at least 15 full cycles of the machine. Once the data has been collected, rename the videos with the following convention:

camera_w_m_c_k_n.mp4

where:
w is the value of the rate of excitation.
m is the weight of the mass on the end of the spring.
c is the damping setting on the damper.
k is the spring constant that you used.
n is the trail number with these settings (if there are mulitple).

Once the videos are named correctly move them into the input folder. Ensure that only the data with this trial is in the folder (so the file names should be identical except for w which changes from video to video). If there already were videos in the input folder, be sure to move them or delete them otherwise the code will process them too.

Once these steps have been completed run the script. to run the script, go to the command line in a linux environment  and type:

python3 VideoProcessor.py

It should output the data for the displacement transmissibility function into graphs and videos in the output folder. In addition, it will output the data for the displacement transmissibility function into 3 arrays that are printed to command line in case they are wanted in another program. They are, in order: the w value, the corresponding displacement transmissibility, and the corresponding error associated with the measurement.
