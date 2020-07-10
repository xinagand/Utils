import subprocess




subprocess.call('ffmpeg -i ./Data/Video_test/Normal_video/amber_180524_000000.avi -ss  30600  -t  3600  -vcodec copy -acodec copy  clip.avi')
subprocess.call('ffmpeg -i ./Data/Video_test/Normal_video/amber_180524_000000.avi -ss  63000  -t  3600  -vcodec copy -acodec copy  clip2.avi')



