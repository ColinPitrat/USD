#!/pxrpythonsubst
#
# Copyright 2017 Pixar
#
# Licensed under the Apache License, Version 2.0 (the "Apache License")
# with the following modification; you may not use this file except in
# compliance with the Apache License and the following modification to it:
# Section 6. Trademarks. is deleted and replaced with:
#
# 6. Trademarks. This License does not grant permission to use the trade
#    names, trademarks, service marks, or product names of the Licensor
#    and its affiliates, except as required to comply with Section 4(c) of
#    the License and to reproduce the content of the NOTICE file.
#
# You may obtain a copy of the Apache License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Apache License with the above modification is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Apache License for the specific
# language governing permissions and limitations under the Apache License.

from pxr import Ar, Sdf, Usd, UsdUtils

import argparse, contextlib, sys

@contextlib.contextmanager
def stream(path, *args, **kwargs):
    if path == '-':
        yield sys.stdout
    else:
        with open(path, *args, **kwargs) as fp:
            yield fp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('usdzFile')
    parser.add_argument('assetPath')
    parser.add_argument('-l', '--listContents', type=str, default='-', 
                        dest='outfile')

    args = parser.parse_args()

    Ar.GetResolver().CreateDefaultContextForAsset(args.assetPath)
    assert UsdUtils.CreateNewUsdzPackage(Sdf.AssetPath(args.assetPath), 
                                         args.usdzFile)

    zipFile = Usd.ZipFile.Open(args.usdzFile)
    assert zipFile

    with stream(args.outfile, 'w') as ofp:
        for fileName in zipFile.GetFileNames():
            print >>ofp, fileName