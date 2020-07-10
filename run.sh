


foldname=./Data/Video_test/Normal_video/

num=0
for LINE in `ls $foldname`
do
  echo $LINE
  file_path=$foldname$LINE
  echo $file_path
  ffmpeg  -i $file_path -ss  30600  -t  3600  -vcodec copy -acodec copy  normal_$num.mp4
  let "num += 1"
  ffmpeg  -i $file_path -ss  63000  -t  3600  -vcodec copy -acodec copy  normal_$num.mp4
  let "num += 1"
done

