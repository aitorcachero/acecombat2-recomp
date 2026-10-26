cmake_minimum_required(VERSION 3.20)
set(PSXRECOMP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/psxrecomp" CACHE PATH
    "Path to psxrecomp")
if(NOT EXISTS "${PSXRECOMP_ROOT}/runtime/runtime.cmake")
    message(FATAL_ERROR
        "PSXRecomp runtime is missing: ${PSXRECOMP_ROOT}/runtime/runtime.cmake\n"
        "This project expects the psxrecomp framework checkout at ${PSXRECOMP_ROOT}.")
endif()

project(AceCombat2Recomp LANGUAGES C CXX)

set(PSX_SETUP_WIZARD ON CACHE BOOL
    "Advertise first-run setup wizard + Generate & rebuild in recomp-ui" FORCE)
set(PSX_GL_BATCH_IMPL "HLE" CACHE STRING "OpenGL textured batching" FORCE)
include("${PSXRECOMP_ROOT}/runtime/runtime.cmake")

set(PSX_PRELOADED_MODS "${CMAKE_CURRENT_SOURCE_DIR}/mods/preloaded")
if(NOT IS_DIRECTORY "${PSX_PRELOADED_MODS}")
    set(PSX_PRELOADED_MODS "NONE")
endif()

psxrecomp_add_game_runtime(psx-runtime
    PRELOADED_MODS_DIR "${PSX_PRELOADED_MODS}"
    ENABLE_SETUP_WIZARD
    WINDOW_TITLE "Ace Combat 2 Recompiled"
    DEFAULT_GAME_CONFIG_PATH "game.toml"
    MAX_PLAYERS 1
    APP_ICON "${CMAKE_CURRENT_SOURCE_DIR}/psxrecomp/assets/psxrecomp.ico"
    GEN_MARKER "generated/SCES_006.99_dispatch.c"
    GEN_FULL_GLOB "generated/SCES_006.99_full_*.c"
    CODEGEN_SETUP_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/codegen_setup.c"
)

foreach(_PSX_RUNTIME_CONFIG game.toml game_options.toml)
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${_PSX_RUNTIME_CONFIG}")
        add_custom_command(TARGET psx-runtime POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
                "${CMAKE_CURRENT_SOURCE_DIR}/${_PSX_RUNTIME_CONFIG}"
                "$<TARGET_FILE_DIR:psx-runtime>/${_PSX_RUNTIME_CONFIG}"
            COMMENT "Staging ${_PSX_RUNTIME_CONFIG}"
            VERBATIM)
    endif()
endforeach()
