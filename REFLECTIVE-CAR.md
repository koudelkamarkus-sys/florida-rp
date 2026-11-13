# Reflective Interceptor — source, credits and checks

Original midnight-blue police supercar. Preserves previous model. Editable model model-source/florida-interceptor-reflective.blend. Rebuild with Blender5.2.2LTS: Blender --background --python model-source/generate_interceptor_reflective.py . Keep all four generator scripts together. HDR expected at dist/environments/suburban-parking-1k.hdr.

Metallic lacquer with full clearcoat, low roughness reflective glass, polished rims, ivory police lettering, trapezoidal radiator grille, finer grillemesh/wiper/trim. Body surfacing still simplified compared with professional automotive assets; not a photorealistic scan. Final GLB3452260bytes151410triangles. Separate body/wheels/frontsteer rig preserved, wheelradius.355m wheelbase2.76m. Route unchanged.

HDR: Suburban Parking Area by Jacopo Voltolina / Poly Haven, CC0,1341401bytes. https://polyhaven.com/a/suburban_parking_area ; https://polyhaven.com/license . No purchased assets or thirdparty car geometry. Three.jsr180/HDRLoader MIT; library licence retained in site vendor folder. Reflection is an environment map, not a realtime reflection of page photographs. Research: https://archive.threejs.org/docs/api/en/materials/MeshPhysicalMaterial.html ; https://threejs.org/manual/pages/materials.html .

Runtime: HDR plus PMREM with studiofallback on failed HDRload. Lowered fill for contrast, per-material reflectionintensity. Same-model staticPNGfallback rebuilt. Modelsource/GLB and front/side/threequarter previews preserved as siblings. No Hyper3D key configured, so no APIcall or charge.

Actual checks: allthree Blender renders inspected; rigvalidator passed; route puretests passed. Browser HDRandmodel loaded with noerrorlogs, stopreadingssame, reverseprogresszero, midwayreload exactposeequality. 390pxiframe loaded/nooverflow (not a physicalphone/FPSbenchmark). Motionofffallback loaded thenrestored; Discorddialogopenedclosed. HDRfailurecatch implemented notinduced; no OSreducedmotion orcontextloss test. Rain/backgrounds unchanged.
