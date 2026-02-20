from spack.package import *


class Edepsim(CMakePackage):
    """An energy deposition simulation based on G4. The default output is a ROOT tree, but the simulation can also be directly called as a library."""

    homepage = "https://github.com/ClarkMcGrew/edep-sim"
    git = "https://github.com/ClarkMcGrew/edep-sim.git"
    url = "https://github.com/ClarkMcGrew/edep-sim/archive/refs/tags/3.2.0.tar.gz"

    maintainers("brettviren")

    license("MIT")

    version("master", branch="master")
    version("3.2.0", sha256="119a5b274601cf721d4f954dee8191e089f157b7b9feb97b10e6a1de399f7771")
    version("3.1.0", sha256="7ac82d4ef30259b98b82b7d6bca4e556b5c1f65a4e7b9f7bd24df2304ebdd97e")
    version("3.0.0", sha256="b91343f986ecb66505de813c6221a74c42d3635c4bb9bfe947cf6a1ac397bc15")
    version("2.0.1", sha256="3017fdbe8047dce970004d6a185191d0d85864e772af33f7438b0b694076761e")
    version("2.0.0", sha256="f38e6d22e86b84103f00a3c2c49a5cea399ab102926a6e389205f0aeef8695e7")

    depends_on("root@6.28.12:")
    depends_on("geant4@10.6.1:")

