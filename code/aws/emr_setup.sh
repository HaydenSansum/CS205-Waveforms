cd /usr/local/bin
sudo wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
sudo wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5
sudo tar xvf ffmpeg-git-amd64-static.tar.xz
sudo mv ffmpeg-git-20200504-amd64-static/ffmpeg ffmpeg-git-20200504-amd64-static/ffprobe /usr/local/bin/
sudo ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
cd ~
echo "export PATH=~/usr/local/bin:$PATH" >>~/.bash_profile
echo "export PATH=~/.local/bin:$PATH" >>~/.bash_profile
echo "export PATH=~/usr/local/bin/ffmpeg:$PATH" >>~/.bash_profile
echo "export PATH=/usr/local/bin:$PATH" >>~/.bash_profile
echo "export PATH=/usr/local/bin/ffmpeg:$PATH" >>~/.bash_profile
echo "export PATH=/usr/bin:$PATH" >>~/.bash_profile
echo "export PATH=/usr/bin/ffmpeg:$PATH" >>~/.bash_profile
source ~/.bash_profile
sudo pip install --upgrade pip
sudo pip install wheel
sudo yum install numba
sudo pip install -r emr_requirements_preprocessing.txt
File
