
# shamelessly stolen from: https://www.pyimagesearch.com/2017/11/27/image-hashing-opencv-python/

from imutils import paths
import argparse
import time
import sys
import cv2
import os
from multiprocessing import Pool

# 1234
# abcd

def dhash(image, hash_size=8):
	'''resizes image to hash_size+1 x hash_size'''
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hash_size + 1, hash_size))
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash

	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--haystack", required=True,
        help="dataset of images to search through (i.e., the haytack)")
    ap.add_argument("-n", "--needles", required=True,
        help="set of images we are searching for (i.e., needles)")
    args = vars(ap.parse_args())

    print("[INFO] computing hashes for haystack...")
    haystack_paths = list(paths.list_images(args["haystack"]))
    needle_paths = list(paths.list_images(args["needles"]))

    BASE_PATHS = set([p.split(os.path.sep)[-2] for p in needle_paths])
    haystack = {}
    hashes = {}

    start = time.time()
    def my_fun(p):
        image = cv2.imread(p)
        # if the image is None then we could not load it from disk (so
        # skip it)
        if image is None:
            return None, None
        # convert the image to grayscale and compute the hash
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_hash = dhash(image)
        return p, image_hash

    with Pool(4) as pool:
        for p, image_hash in pool.map(my_fun, haystack_paths):
            if p is None:
                continue
            if image_hash is None:
                continue
            if image_hash in hashes:
                hashes[image_hash].append(p)
            else:
                hashes[image_hash] = [p]
            # update the haystack dictionary
            l = haystack.get(image_hash, [])
            l.append(p)
            haystack[image_hash] = l

    print("[INFO] processed {} images in {:.2f} seconds".format(
        len(haystack), time.time() - start))
    print("[INFO] computing hashes for needles...")

    start = time.time()

    with Pool(4) as pool:
        for p, image_hash in pool.map(my_fun, needle_paths):
            if p is None:
                continue
            if image_hash is None:
                continue
            if image_hash in hashes:
                hashes[image_hash].append(p)
            else:
                hashes[image_hash] = [p]
            # grab all image paths that match the hash
            matched_paths = haystack.get(image_hash, [])
            # loop over all matched paths
            for matched_path in matched_paths:
                # extract the subdirectory from the image path
                b = p.split(os.path.sep)[-2]
                # if the subdirectory exists in the base path for the needle
                # images, remove it
                if b in BASE_PATHS:
                    BASE_PATHS.remove(b)

    print("[INFO] processed {} images in {:.2f} seconds".format(
        len(needle_paths), time.time() - start))

    for i in hashes:
        if len(hashes[i]) > 1:
            print(i, hashes[i])

# vim: ai sw=4 ts=4 et showmatch
