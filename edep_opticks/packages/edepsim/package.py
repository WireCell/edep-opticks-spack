from spack.package import *


class Edepsim(CMakePackage):
    """An energy deposition simulation based on G4. The default output is a ROOT tree, but the simulation can also be directly called as a library."""

    homepage = "https://github.com/ClarkMcGrew/edep-sim"
    git = "https://github.com/ClarkMcGrew/edep-sim.git"
    url = "https://github.com/ClarkMcGrew/edep-sim/archive/refs/tags/3.2.0.tar.gz"

    maintainers("brettviren")

    license("MIT")

    # Fixme: we do not even attempt to support old releases up to and including 3.2.0
    version("master", branch="master")

    depends_on("cmake@3.30:", type="build", when="@master")

    # C++

    cxxstds = ('11', '14', '17', '20')
    variant('cxxstd', default='17', values=cxxstds, multi=False, description='C++ standard')

    # Pass on the C++ standard to dependencies via "anonymous constraint"
    for std in cxxstds:
        depends_on(f"root@ 6.28.12: cxxstd={std}", when=f'cxxstd={std}')
        depends_on(f"geant4 @10.6.1: cxxstd={std}", when=f'cxxstd={std}')
        depends_on(f"eicopticks @main cxxstd={std}", when=f'+opticks cxxstd={std}')

    variant('opticks', default=False, when="@master",
            description='Add support for eic-opticks for GPU accelerated photon transport')

    def cmake_args(self):
        # Map the variant value to the standard CMake variable
        return [
            f"-DCMAKE_CXX_STANDARD={self.spec.variants['cxxstd'].value}"
        ]
