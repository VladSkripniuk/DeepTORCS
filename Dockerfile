FROM tensorflow/tensorflow:latest-devel-gpu
MAINTAINER github/skripniuk

RUN apt-get update && apt-get install -y cmake libgtk2.0-dev && \
	git clone --depth 1 https://github.com/opencv/opencv.git && \
	cd opencv && \
	mkdir build && \
	cd build && \
	cmake -D WITH_CUDA=OFF -D WITH_GTK=ON .. && \
	make -j"$(nproc)"  && \
	make install && \
	ldconfig

RUN apt-get update; \
	apt-get install -y cmake mesa-utils kmod binutils; \ 
	apt-get install -y libalut-dev libvorbis-dev cmake libxrender-dev libxrender1 libxrandr-dev zlib1g-dev libpng16-dev; \
	apt-get install -y freeglut3 freeglut3-dev; \
	apt-get install -y libxmu-dev libxmu6 libxi-dev; \
	apt-get install -y wget

# install PLIB-1.8.5
RUN wget http://plib.sourceforge.net/dist/plib-1.8.5.tar.gz; \
	tar xfvz plib-1.8.5.tar.gz; \
	ln -s /usr/lib/libGL.so.1 /usr/lib/libGL.so

# PLIB should be compiled with "-fPIC"
RUN cd plib-1.8.5; \
	export CFLAGS="-fPIC"; \
	export CPPFLAGS=$CFLAGS; \
	export CXXFLAGS=$CFLAGS; \
	./configure; \
	make install

# install openal-1.17.2
RUN wget http://kcat.strangesoft.net/openal-releases/openal-soft-1.17.2.tar.bz2; \
	apt-get install bzip2; \
	tar xfvj openal-soft-1.17.2.tar.bz2; \
	cd openal-soft-1.17.2/build; \
	cmake ..; \
	make; \
	make install

ADD torcs-1.3.6 torcs-1.3.6

RUN cd torcs-1.3.6; \
	make; \
	make install; \
	make datainstall

ADD modified_tracks /usr/local/share/games/torcs/tracks/road

RUN chmod -R +rwx /usr/local/share/games/torcs/tracks/road/ 
