from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class EdepSimphonyPlugin(CMakePackage):
    """edep-sim + Simphony GPU optical-photon integration plugin.

    A Geant4 user-action plugin (libedep-simphony-plugin.so) loaded into
    edep-sim via its EXTERN mechanism.  It hands Cerenkov/Scintillation
    gensteps to Simphony for GPU (NVIDIA OptiX) optical-photon transport and
    writes the GPU photon trees into the edep-sim ROOT output file.
    """

    homepage = "https://github.com/brettviren/edep-simphony-plugin"
    git = "https://github.com/brettviren/edep-simphony-plugin.git"

    maintainers("brettviren")

    # No LICENSE file is present in the upstream repo yet.

    version("master", branch="master")

    depends_on("cmake@3.18:", type="build")

    # C++
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    # simphony caps at C++23 (its own code targets 17 but the variant accepts up
    # to 23 so it can share a higher-standard geant4/root); the plugin links
    # simphony, so it offers the same set.
    cxxstds = ("17", "20", "23")
    variant("cxxstd", default="17", values=cxxstds, multi=False, description="C++ standard")

    # Unify the C++ standard across every ABI-sharing dependency.  edep-sim, root
    # and geant4 track the same value simphony is built with.
    for std in cxxstds:
        depends_on(f"root cxxstd={std}", when=f"cxxstd={std}")
        depends_on(f"geant4 cxxstd={std}", when=f"cxxstd={std}")
        depends_on(f"edepsim cxxstd={std}", when=f"cxxstd={std}")
        depends_on(f"simphony cxxstd={std}", when=f"cxxstd={std}")

    def cmake_args(self):
        # The adapted CMakeLists finds everything via CMAKE_PREFIX_PATH; the only
        # knob it needs is the C++ standard (otherwise it inherits ROOT's).
        return [
            self.define("CMAKE_CXX_STANDARD", self.spec.variants["cxxstd"].value),
        ]

    @run_after("install")
    def install_macros(self):
        # The CMakeLists installs only the .so, so carry the run macros too.
        install_tree(
            join_path(self.stage.source_path, "macro"),
            join_path(self.prefix.share, "edep-simphony-plugin", "macro"),
        )

    def setup_run_environment(self, env):
        lib = join_path(self.prefix.lib, "libedep-simphony-plugin.so")
        # The shipped run macros load the plugin actions via $(PLUGIN_LIB).
        env.set("PLUGIN_LIB", lib)
        # Load the plugin's instrumented Cerenkov/Scintillation physics into
        # edep-sim (EXTERN:<lib>:<factory>).
        env.set("EXTRAPHYSICS", f"EXTERN:{lib}:CreatePhysicsConstructor")
        # GPU-only integration mode (CPU optical photons killed).
        env.set("OPTICKS_INTEGRATION_MODE", "1")
        # PTX ray-tracing kernel built and installed by simphony.
        env.set(
            "CSGOptiX__ptxpath",
            join_path(self.spec["simphony"].prefix.lib, "CSGOptiX7.ptx"),
        )
        # Reasonable debug-scale defaults; raise for production runs.
        env.set("OPTICKS_MAX_SLOT", "M1")
        env.set("EDEPSIM_DOKEBIRKS_VISE", "1")
        # The EDEP_SIMPHONY_* run-mode knobs are intentionally left user-set.
