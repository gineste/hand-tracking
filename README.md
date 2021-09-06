# Reconnaissance de la main et tracking de points 

Ce repo propose la mise en oeuvre de scripts simples inspirés du tutoriel de la chaine youtube de robotique et AI *Murtaza videos* voir ici:
https://www.youtube.com/watch?v=NZde8Xt78Iw

La bibliothèque python mediapipe (avec cv2 pour l'acquisition video) fournit tous les outils nécessaires, et existe sur windows ou raspberry, les deux ont été testés. Le réseau de neurone est déjà entrainé;

# calcul de métriques

la librairie permet de calculer des métriques sur des points particuliers de la main.
(à venir)

# installation sur raspberry (4)

`sudo apt-get update` \
`pip3 install ffmpeg opencv-python` \
`sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23` \
numpy était trop vieux et pas compatible donc:
`pip3 install numpy --upgrade` \

Là ca doit fonctionner. 
