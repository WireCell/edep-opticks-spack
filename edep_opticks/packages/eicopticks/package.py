# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class Eicopticks(CMakePackage, CudaPackage):
    """GPU-Accelerated Optical Photon Simulation using NVIDIA OptiX"""

    homepage = "https://github.com/bnlnpps/eic-opticks"
    git = "https://github.com/bnlnpps/eic-opticks.git"

    license("Apache-2.0")

    maintainers("plexoos")

    version("main", branch="main")

    depends_on("cmake@3.10:", type="build")
    depends_on("cxx", type="build")

    # C++
    depends_on("cxx", type="build")
    # Verison 17 is hard-wired in the CMakeLists.txt file
    cxxstds = ('17',)
    variant('cxxstd', default='17', values=cxxstds, multi=False, description='C++ standard')

    for std in cxxstds:
        depends_on(f"geant4@11.3.2: cxxstd={std}", when=f'cxxstd={std}')

    # C++ but does not use cxxstd
    depends_on("nlohmann-json")
    depends_on("plog")

    depends_on("cuda")
    depends_on("glew")
    depends_on("glfw")
    depends_on("glm")
    depends_on("glu")
    depends_on("mesa")
    depends_on("optix-dev")
    depends_on("openssl")

    depends_on("python")

    def cmake_args(self):
        # Map the variant value to the standard CMake variable
        return [
            f"-DCMAKE_CXX_STANDARD={self.spec.variants['cxxstd'].value}"
        ]
    
