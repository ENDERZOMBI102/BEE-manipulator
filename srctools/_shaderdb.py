def _shader_db(var_type, DB):
    [FLAG, MATERIAL, STR, TEXTURE, INT, FLOAT, BOOL, COLOR, VEC2, VEC3, VEC4, MATRIX, FOUR_CC] = var_type
    DB['%compile2dsky'] = FLAG
    DB['%compileblocklos'] = FLAG
    DB['%compileclip'] = FLAG
    DB['%compiledetail'] = FLAG
    DB['%compilefog'] = FLAG
    DB['%compilegrenadeclip'] = FLAG
    DB['%compilehint'] = FLAG
    DB['%compileladder'] = FLAG
    DB['%compilenochop'] = FLAG
    DB['%compilenodraw'] = FLAG
    DB['%compilenolight'] = FLAG
    DB['%compilenonsolid'] = FLAG
    DB['%compilenpcclip'] = FLAG
    DB['%compileorigin'] = FLAG
    DB['%compilepassbullets'] = FLAG
    DB['%compileskip'] = FLAG
    DB['%compilesky'] = FLAG
    DB['%compileslime'] = FLAG
    DB['%compileteam'] = FLAG
    DB['%compiletrigger'] = FLAG
    DB['%compilewater'] = FLAG
    DB['%nopaint'] = FLAG
    DB['%noportal'] = FLAG
    DB['%notooltexture'] = FLAG
    DB['%playerclip'] = FLAG
    DB['additive'] = FLAG
    DB['allowalphatocoverage'] = FLAG
    DB['alphatest'] = FLAG
    DB['basealphaenvmapmask'] = FLAG
    DB['debug'] = FLAG
    DB['decal'] = FLAG
    DB['envmapcameraspace'] = FLAG
    DB['envmapmode'] = FLAG
    DB['envmapsphere'] = FLAG
    DB['flat'] = FLAG
    DB['halflambert'] = FLAG
    DB['ignorez'] = FLAG
    DB['model'] = FLAG
    DB['multipass'] = FLAG
    DB['no_draw'] = FLAG
    DB['no_fullbright'] = FLAG
    DB['noalphamod'] = FLAG
    DB['nocull'] = FLAG
    DB['nodecal'] = FLAG
    DB['nofog'] = FLAG
    DB['normalmapalphaenvmapmask'] = FLAG
    DB['notint'] = FLAG
    DB['opaquetexture'] = FLAG
    DB['selfillum'] = FLAG
    DB['softwareskin'] = FLAG
    DB['translucent'] = FLAG
    DB['use_in_fillrate_mode'] = FLAG
    DB['vertexalpha'] = FLAG
    DB['wireframe'] = FLAG
    DB['znearer'] = FLAG

    DB['bottommaterial'] = MATERIAL
    DB['crackmaterial'] = MATERIAL
    DB['translucent_material'] = MATERIAL

    DB['%detailtype'] = STR
    DB['%keywords'] = STR
    DB['fallback'] = STR
    DB['pixshader'] = STR
    DB['surfaceprop'] = STR
    DB['surfaceprop2'] = STR
    DB['vertexshader'] = STR

    DB['%tooltexture'] = TEXTURE
    DB['albedo'] = TEXTURE
    DB['alphamasktexture'] = TEXTURE
    DB['ambientoccltexture'] = TEXTURE
    DB['basetexture'] = TEXTURE
    DB['basetexture2'] = TEXTURE
    DB['basetexture3'] = TEXTURE
    DB['basetexture4'] = TEXTURE
    DB['basettexture'] = TEXTURE
    DB['blendmodulatetexture'] = TEXTURE
    DB['bloomtexture'] = TEXTURE
    DB['blurredtexture'] = TEXTURE
    DB['blurtexture'] = TEXTURE
    DB['bumpcompress'] = TEXTURE
    DB['bumpmap'] = TEXTURE
    DB['bumpmap2'] = TEXTURE
    DB['bumpmask'] = TEXTURE
    DB['bumpstretch'] = TEXTURE
    DB['cbtexture'] = TEXTURE
    DB['cloudalphatexture'] = TEXTURE
    DB['colorwarptexture'] = TEXTURE
    DB['compress'] = TEXTURE
    DB['cookietexture'] = TEXTURE
    DB['corecolortexture'] = TEXTURE
    DB['corneatexture'] = TEXTURE
    DB['crtexture'] = TEXTURE
    DB['delta'] = TEXTURE
    DB['depthtexture'] = TEXTURE
    DB['detail'] = TEXTURE
    DB['detail1'] = TEXTURE
    DB['detail2'] = TEXTURE
    DB['displacementmap'] = TEXTURE
    DB['dudvmap'] = TEXTURE
    DB['dust_texture'] = TEXTURE
    DB['effectmaskstexture'] = TEXTURE
    DB['emissiveblendbasetexture'] = TEXTURE
    DB['emissiveblendflowtexture'] = TEXTURE
    DB['emissiveblendtexture'] = TEXTURE
    DB['envmap'] = TEXTURE
    DB['envmapmask'] = TEXTURE
    DB['exposure_texture'] = TEXTURE
    DB['fb_texture'] = TEXTURE
    DB['fbtexture'] = TEXTURE
    DB['fleshbordertexture1d'] = TEXTURE
    DB['fleshcubetexture'] = TEXTURE
    DB['fleshinteriornoisetexture'] = TEXTURE
    DB['fleshinteriortexture'] = TEXTURE
    DB['fleshnormaltexture'] = TEXTURE
    DB['fleshsubsurfacetexture'] = TEXTURE
    DB['flow_noise_texture'] = TEXTURE
    DB['flowbounds'] = TEXTURE
    DB['flowmap'] = TEXTURE
    DB['fow'] = TEXTURE
    DB['frametexture'] = TEXTURE
    DB['fresnelcolorwarptexture'] = TEXTURE
    DB['fresnelrangestexture'] = TEXTURE
    DB['fresnelwarptexture'] = TEXTURE
    DB['glassenvmap'] = TEXTURE
    DB['glint'] = TEXTURE
    DB['gradienttexture'] = TEXTURE
    DB['grain'] = TEXTURE
    DB['grain_texture'] = TEXTURE
    DB['hdrbasetexture'] = TEXTURE
    DB['hdrcompressedtexture'] = TEXTURE
    DB['hdrcompressedtexture0'] = TEXTURE
    DB['hdrcompressedtexture1'] = TEXTURE
    DB['hdrcompressedtexture2'] = TEXTURE
    DB['input'] = TEXTURE
    DB['input_texture'] = TEXTURE
    DB['internal_vignettetexture'] = TEXTURE
    DB['iridescentwarp'] = TEXTURE
    DB['iris'] = TEXTURE
    DB['lightwarptexture'] = TEXTURE
    DB['maps1'] = TEXTURE
    DB['maps2'] = TEXTURE
    DB['maps3'] = TEXTURE
    DB['noisetexture'] = TEXTURE
    DB['normalmap'] = TEXTURE
    DB['normalmap2'] = TEXTURE
    DB['opacitytexture'] = TEXTURE
    DB['originaltexture'] = TEXTURE
    DB['paintsplatenvmap'] = TEXTURE
    DB['paintsplatnormalmap'] = TEXTURE
    DB['phongexponenttexture'] = TEXTURE
    DB['phongwarptexture'] = TEXTURE
    DB['portalcolortexture'] = TEXTURE
    DB['portalmasktexture'] = TEXTURE
    DB['ramptexture'] = TEXTURE
    DB['reflecttexture'] = TEXTURE
    DB['refracttexture'] = TEXTURE
    DB['refracttinttexture'] = TEXTURE
    DB['screeneffecttexture'] = TEXTURE
    DB['selfillummap'] = TEXTURE
    DB['selfillummask'] = TEXTURE
    DB['selfillumtexture'] = TEXTURE
    DB['shadowdepthtexture'] = TEXTURE
    DB['sidespeed'] = TEXTURE
    DB['smallfb'] = TEXTURE
    DB['sourcemrtrendertarget'] = TEXTURE
    DB['spectexture'] = TEXTURE
    DB['spectexture2'] = TEXTURE
    DB['spectexture3'] = TEXTURE
    DB['spectexture4'] = TEXTURE
    DB['staticblendtexture'] = TEXTURE
    DB['stretch'] = TEXTURE
    DB['texture0'] = TEXTURE
    DB['texture1'] = TEXTURE
    DB['texture2'] = TEXTURE
    DB['texture3'] = TEXTURE
    DB['texture4'] = TEXTURE
    DB['transmatmaskstexture'] = TEXTURE
    DB['underwateroverlay'] = TEXTURE
    DB['velocity_texture'] = TEXTURE
    DB['ytexture'] = TEXTURE

    DB['addoverblend'] = INT
    DB['alpha_blend'] = INT
    DB['alpha_blend_color_overlay'] = INT
    DB['alphablend'] = INT
    DB['alphadepth'] = INT
    DB['alphamasktextureframe'] = INT
    DB['ambientboostmaskmode'] = INT
    DB['ambientonly'] = INT
    DB['basemapalphaphongmask'] = INT
    DB['basemapluminancephongmask'] = INT
    DB['bloomtintenable'] = INT
    DB['bloomtype'] = INT
    DB['bluramount'] = INT
    DB['bumpframe'] = INT
    DB['bumpframe2'] = INT
    DB['clearalpha'] = INT
    DB['clearcolor'] = INT
    DB['cleardepth'] = INT
    DB['cookieframenum'] = INT
    DB['copyalpha'] = INT
    DB['corecolortextureframe'] = INT
    DB['cull'] = INT
    DB['depthblend'] = INT
    DB['depthtest'] = INT
    DB['desaturateenable'] = INT
    DB['detail1blendmode'] = INT
    DB['detail1frame'] = INT
    DB['detail2blendmode'] = INT
    DB['detail2frame'] = INT
    DB['detailblendmode'] = INT
    DB['detailframe'] = INT
    DB['disable_color_writes'] = INT
    DB['dualsequence'] = INT
    DB['dudvframe'] = INT
    DB['enableshadows'] = INT
    DB['envmapframe'] = INT
    DB['envmapmaskframe'] = INT
    DB['extractgreenalpha'] = INT
    DB['fade'] = INT
    DB['flowmapframe'] = INT
    DB['frame'] = INT
    DB['frame2'] = INT
    DB['frame3'] = INT
    DB['gammacolorread'] = INT
    DB['invertphongmask'] = INT
    DB['irisframe'] = INT
    DB['kernel'] = INT
    DB['linearread_basetexture'] = INT
    DB['linearread_texture1'] = INT
    DB['linearread_texture2'] = INT
    DB['linearread_texture3'] = INT
    DB['linearwrite'] = INT
    DB['maskedblending'] = INT
    DB['maxlumframeblend1'] = INT
    DB['maxlumframeblend2'] = INT
    DB['mirroraboutviewportedges'] = INT
    DB['mode'] = INT
    DB['mrtindex'] = INT
    DB['multiplycolor'] = INT
    DB['nocolorwrite'] = INT
    DB['nodiffusebumplighting'] = INT
    DB['noviewportfixup'] = INT
    DB['nowritez'] = INT
    DB['orientation'] = INT
    DB['parallaxmap'] = INT
    DB['passcount'] = INT
    DB['pointsample_basetexture'] = INT
    DB['pointsample_texture1'] = INT
    DB['pointsample_texture2'] = INT
    DB['pointsample_texture3'] = INT
    DB['quality'] = INT
    DB['receiveflashlight'] = INT
    DB['refracttinttextureframe'] = INT
    DB['renderfixz'] = INT
    DB['selfillumtextureframe'] = INT
    DB['sequence_blend_mode'] = INT
    DB['shadowdepth'] = INT
    DB['singlepassflashlight'] = INT
    DB['splinetype'] = INT
    DB['spriteorientation'] = INT
    DB['spriterendermode'] = INT
    DB['stage'] = INT
    DB['staticblendtextureframe'] = INT
    DB['tcsize0'] = INT
    DB['tcsize1'] = INT
    DB['tcsize2'] = INT
    DB['tcsize3'] = INT
    DB['tcsize4'] = INT
    DB['tcsize5'] = INT
    DB['tcsize6'] = INT
    DB['tcsize7'] = INT
    DB['treesway'] = INT
    DB['tv_gamma'] = INT
    DB['uberlight'] = INT
    DB['usealternateviewmatrix'] = INT
    DB['vertexalphatest'] = INT
    DB['vertexcolor'] = INT
    DB['vertextransform'] = INT
    DB['writealpha'] = INT
    DB['writedepth'] = INT
    DB['x360appchooser'] = INT

    DB['addbasetexture2'] = FLOAT
    DB['addself'] = FLOAT
    DB['alpha'] = FLOAT
    DB['alpha2'] = FLOAT
    DB['alphasharpenfactor'] = FLOAT
    DB['alphatested'] = FLOAT
    DB['alphatestreference'] = FLOAT
    DB['alphatrailfade'] = FLOAT
    DB['ambientboost'] = FLOAT
    DB['ambientocclusion'] = FLOAT
    DB['ambientreflectionboost'] = FLOAT
    DB['autoexpose_max'] = FLOAT
    DB['autoexpose_min'] = FLOAT
    DB['backscatter'] = FLOAT
    DB['blendsoftness'] = FLOAT
    DB['bloomamount'] = FLOAT
    DB['bloomexp'] = FLOAT
    DB['bloomexponent'] = FLOAT
    DB['bloomsaturation'] = FLOAT
    DB['blurredvignettescale'] = FLOAT
    DB['bumpstrength'] = FLOAT
    DB['c0_w'] = FLOAT
    DB['c0_x'] = FLOAT
    DB['c0_y'] = FLOAT
    DB['c0_z'] = FLOAT
    DB['c1_w'] = FLOAT
    DB['c1_x'] = FLOAT
    DB['c1_y'] = FLOAT
    DB['c1_z'] = FLOAT
    DB['c2_w'] = FLOAT
    DB['c2_x'] = FLOAT
    DB['c2_y'] = FLOAT
    DB['c2_z'] = FLOAT
    DB['c3_w'] = FLOAT
    DB['c3_x'] = FLOAT
    DB['c3_y'] = FLOAT
    DB['c3_z'] = FLOAT
    DB['c4_w'] = FLOAT
    DB['c4_x'] = FLOAT
    DB['c4_y'] = FLOAT
    DB['c4_z'] = FLOAT
    DB['cheapwaterenddistance'] = FLOAT
    DB['cheapwaterstartdistance'] = FLOAT
    DB['cloakfactor'] = FLOAT
    DB['color_flow_lerpexp'] = FLOAT
    DB['color_flow_timeintervalinseconds'] = FLOAT
    DB['color_flow_timescale'] = FLOAT
    DB['color_flow_uvscale'] = FLOAT
    DB['color_flow_uvscrolldistance'] = FLOAT
    DB['contrast'] = FLOAT
    DB['corneabumpstrength'] = FLOAT
    DB['decalfadeduration'] = FLOAT
    DB['decalfadetime'] = FLOAT
    DB['decalscale'] = FLOAT
    DB['deltascale'] = FLOAT
    DB['depthblendscale'] = FLOAT
    DB['depthblurfocaldistance'] = FLOAT
    DB['depthblurstrength'] = FLOAT
    DB['desaturatewithbasealpha'] = FLOAT
    DB['desaturation'] = FLOAT
    DB['detailblendfactor'] = FLOAT
    DB['detailscale'] = FLOAT
    DB['diffuseexponent'] = FLOAT
    DB['diffusesoftnormal'] = FLOAT
    DB['dilation'] = FLOAT
    DB['edge_softness'] = FLOAT
    DB['edgesoftnessend'] = FLOAT
    DB['edgesoftnessstart'] = FLOAT
    DB['emissiveblendstrength'] = FLOAT
    DB['endfadesize'] = FLOAT
    DB['envmapcontrast'] = FLOAT
    DB['envmapfresnel'] = FLOAT
    DB['envmaplightscale'] = FLOAT
    DB['envmapmaskscale'] = FLOAT
    DB['envmapsaturation'] = FLOAT
    DB['eyeballradius'] = FLOAT
    DB['fadetoblackscale'] = FLOAT
    DB['falloffamount'] = FLOAT
    DB['falloffdistance'] = FLOAT
    DB['falloffoffset'] = FLOAT
    DB['farblurdepth'] = FLOAT
    DB['farblurradius'] = FLOAT
    DB['farfadeinterval'] = FLOAT
    DB['farfocusdepth'] = FLOAT
    DB['farplane'] = FLOAT
    DB['flashlighttime'] = FLOAT
    DB['flashlighttint'] = FLOAT
    DB['fleshbordernoisescale'] = FLOAT
    DB['fleshbordersoftness'] = FLOAT
    DB['fleshborderwidth'] = FLOAT
    DB['fleshglobalopacity'] = FLOAT
    DB['fleshglossbrightness'] = FLOAT
    DB['fleshscrollspeed'] = FLOAT
    DB['flow_bumpstrength'] = FLOAT
    DB['flow_noise_scale'] = FLOAT
    DB['flow_normaluvscale'] = FLOAT
    DB['flow_timeintervalinseconds'] = FLOAT
    DB['flow_timescale'] = FLOAT
    DB['flow_uvscrolldistance'] = FLOAT
    DB['flow_worlduvscale'] = FLOAT
    DB['flowmaptexcoordoffset'] = FLOAT
    DB['fogend'] = FLOAT
    DB['fogexponent'] = FLOAT
    DB['fogscale'] = FLOAT
    DB['fogstart'] = FLOAT
    DB['forcefresnel'] = FLOAT
    DB['forwardscatter'] = FLOAT
    DB['fresnelbumpstrength'] = FLOAT
    DB['fresnelpower'] = FLOAT
    DB['fresnelreflection'] = FLOAT
    DB['glossiness'] = FLOAT
    DB['glowalpha'] = FLOAT
    DB['glowend'] = FLOAT
    DB['glowstart'] = FLOAT
    DB['glowx'] = FLOAT
    DB['glowy'] = FLOAT
    DB['groundmax'] = FLOAT
    DB['groundmin'] = FLOAT
    DB['hdrcolorscale'] = FLOAT
    DB['height_scale'] = FLOAT
    DB['hueshiftfresnelexponent'] = FLOAT
    DB['hueshiftintensity'] = FLOAT
    DB['illumfactor'] = FLOAT
    DB['interiorambientscale'] = FLOAT
    DB['interiorbackgroundboost'] = FLOAT
    DB['interiorbacklightscale'] = FLOAT
    DB['interiorfogstrength'] = FLOAT
    DB['interiorrefractblur'] = FLOAT
    DB['interiorrefractstrength'] = FLOAT
    DB['iridescenceboost'] = FLOAT
    DB['iridescenceexponent'] = FLOAT
    DB['layerborderoffset'] = FLOAT
    DB['layerbordersoftness'] = FLOAT
    DB['layerborderstrength'] = FLOAT
    DB['lightmaptint'] = FLOAT
    DB['localcontrastedgescale'] = FLOAT
    DB['localcontrastmidtonemask'] = FLOAT
    DB['localcontrastscale'] = FLOAT
    DB['localcontrastvignetteend'] = FLOAT
    DB['localrefractdepth'] = FLOAT
    DB['magnifyscale'] = FLOAT
    DB['mappingheight'] = FLOAT
    DB['mappingwidth'] = FLOAT
    DB['maps1alpha'] = FLOAT
    DB['maxdistance'] = FLOAT
    DB['maxfalloffamount'] = FLOAT
    DB['maxlight'] = FLOAT
    DB['maxreflectivity'] = FLOAT
    DB['maxsize'] = FLOAT
    DB['minlight'] = FLOAT
    DB['minreflectivity'] = FLOAT
    DB['minsize'] = FLOAT
    DB['nearblurdepth'] = FLOAT
    DB['nearblurradius'] = FLOAT
    DB['nearfocusdepth'] = FLOAT
    DB['nearplane'] = FLOAT
    DB['noisestrength'] = FLOAT
    DB['normal2softness'] = FLOAT
    DB['num_lookups'] = FLOAT
    DB['numplanes'] = FLOAT
    DB['outlinealpha'] = FLOAT
    DB['outlineend0'] = FLOAT
    DB['outlineend1'] = FLOAT
    DB['outlinestart0'] = FLOAT
    DB['outlinestart1'] = FLOAT
    DB['overbrightfactor'] = FLOAT
    DB['parallaxstrength'] = FLOAT
    DB['phong2softness'] = FLOAT
    DB['phongboost'] = FLOAT
    DB['phongexponent'] = FLOAT
    DB['phongexponent2'] = FLOAT
    DB['phongscale'] = FLOAT
    DB['phongscale2'] = FLOAT
    DB['portalcolorscale'] = FLOAT
    DB['portalopenamount'] = FLOAT
    DB['portalstatic'] = FLOAT
    DB['pulserate'] = FLOAT
    DB['radiustrailfade'] = FLOAT
    DB['reflectamount'] = FLOAT
    DB['reflectance'] = FLOAT
    DB['reflectblendfactor'] = FLOAT
    DB['refractamount'] = FLOAT
    DB['rimlightboost'] = FLOAT
    DB['rimlightexponent'] = FLOAT
    DB['rimlightscale'] = FLOAT
    DB['rotation'] = FLOAT
    DB['rotation2'] = FLOAT
    DB['rotation3'] = FLOAT
    DB['rotation4'] = FLOAT
    DB['saturation'] = FLOAT
    DB['scale'] = FLOAT
    DB['scale2'] = FLOAT
    DB['scale3'] = FLOAT
    DB['scale4'] = FLOAT
    DB['screenblurstrength'] = FLOAT
    DB['seamless_scale'] = FLOAT
    DB['selfillum_envmapmask_alpha'] = FLOAT
    DB['selfillummaskscale'] = FLOAT
    DB['shadowatten'] = FLOAT
    DB['shadowfiltersize'] = FLOAT
    DB['shadowjitterseed'] = FLOAT
    DB['sharpness'] = FLOAT
    DB['silhouettethickness'] = FLOAT
    DB['ssbentnormalintensity'] = FLOAT
    DB['ssdepth'] = FLOAT
    DB['sstintbyalbedo'] = FLOAT
    DB['startfadesize'] = FLOAT
    DB['staticamount'] = FLOAT
    DB['time'] = FLOAT
    DB['toolcolorcorrection'] = FLOAT
    DB['tooltime'] = FLOAT
    DB['treeswayfalloffexp'] = FLOAT
    DB['treeswayheight'] = FLOAT
    DB['treeswayradius'] = FLOAT
    DB['treeswayscrumblefalloffexp'] = FLOAT
    DB['treeswayscrumblefrequency'] = FLOAT
    DB['treeswayscrumblespeed'] = FLOAT
    DB['treeswayscrumblestrength'] = FLOAT
    DB['treeswayspeed'] = FLOAT
    DB['treeswayspeedhighwindmultiplier'] = FLOAT
    DB['treeswayspeedlerpend'] = FLOAT
    DB['treeswayspeedlerpstart'] = FLOAT
    DB['treeswaystartheight'] = FLOAT
    DB['treeswaystartradius'] = FLOAT
    DB['treeswaystrength'] = FLOAT
    DB['uberroundness'] = FLOAT
    DB['unlitfactor'] = FLOAT
    DB['uvscale'] = FLOAT
    DB['vertexfogamount'] = FLOAT
    DB['vignette_min_bright'] = FLOAT
    DB['vignette_power'] = FLOAT
    DB['volumetricintensity'] = FLOAT
    DB['vomitrefractscale'] = FLOAT
    DB['warpparam'] = FLOAT
    DB['waterblendfactor'] = FLOAT
    DB['waterdepth'] = FLOAT
    DB['wave'] = FLOAT
    DB['weight0'] = FLOAT
    DB['weight1'] = FLOAT
    DB['weight2'] = FLOAT
    DB['weight3'] = FLOAT
    DB['weight_default'] = FLOAT
    DB['woodcut'] = FLOAT
    DB['zoomanimateseq2'] = FLOAT

    DB['aaenable'] = BOOL
    DB['abovewater'] = BOOL
    DB['addbumpmaps'] = BOOL
    DB['allowdiffusemodulation'] = BOOL
    DB['allowfencerenderstatehack'] = BOOL
    DB['allowlocalcontrast'] = BOOL
    DB['allownoise'] = BOOL
    DB['allowvignette'] = BOOL
    DB['alphaenvmapmask'] = BOOL
    DB['alphatesttocoverage'] = BOOL
    DB['aomaskusesuv2'] = BOOL
    DB['aousesuv2'] = BOOL
    DB['basealphaenvmask'] = BOOL
    DB['basemapalphaenvmapmask'] = BOOL
    DB['basetexture2noenvmap'] = BOOL
    DB['basetexturenoenvmap'] = BOOL
    DB['blendframes'] = BOOL
    DB['blendtintbybasealpha'] = BOOL
    DB['blobbyshadows'] = BOOL
    DB['bloomenable'] = BOOL
    DB['blurredvignetteenable'] = BOOL
    DB['blurrefract'] = BOOL
    DB['bump_force_on'] = BOOL
    DB['bumpbasetexture2withbumpmap'] = BOOL
    DB['cloakpassenabled'] = BOOL
    DB['decalsecondpass'] = BOOL
    DB['deferredshadows'] = BOOL
    DB['depthblurenable'] = BOOL
    DB['detail_alpha_mask_base_texture'] = BOOL
    DB['displacementwrinkle'] = BOOL
    DB['distancealpha'] = BOOL
    DB['distancealphafromdetail'] = BOOL
    DB['emissiveblendenabled'] = BOOL
    DB['enableclearcolor'] = BOOL
    DB['enablesrgb'] = BOOL
    DB['envmapoptional'] = BOOL
    DB['fadeoutonsilhouette'] = BOOL
    DB['flashlightnolambert'] = BOOL
    DB['fleshdebugforcefleshon'] = BOOL
    DB['fleshinteriorenabled'] = BOOL
    DB['flow_debug'] = BOOL
    DB['fogenable'] = BOOL
    DB['forcebump'] = BOOL
    DB['forcecheap'] = BOOL
    DB['forceenvmap'] = BOOL
    DB['forceexpensive'] = BOOL
    DB['forcephong'] = BOOL
    DB['forcerefract'] = BOOL
    DB['glow'] = BOOL
    DB['ignorevertexcolors'] = BOOL
    DB['interior'] = BOOL
    DB['intro'] = BOOL
    DB['inversedepthblend'] = BOOL
    DB['lightmapwaterfog'] = BOOL
    DB['localcontrastenable'] = BOOL
    DB['localcontrastvignettestart'] = BOOL
    DB['localrefract'] = BOOL
    DB['magnifyenable'] = BOOL
    DB['masked'] = BOOL
    DB['mod2x'] = BOOL
    DB['newlayerblending'] = BOOL
    DB['nofresnel'] = BOOL
    DB['noiseenable'] = BOOL
    DB['nolowendlightmap'] = BOOL
    DB['noscale'] = BOOL
    DB['nosrgb'] = BOOL
    DB['opaque'] = BOOL
    DB['outline'] = BOOL
    DB['perparticleoutline'] = BOOL
    DB['phong'] = BOOL
    DB['phongalbedotint'] = BOOL
    DB['phongdisablehalflambert'] = BOOL
    DB['pseudotranslucent'] = BOOL
    DB['raytracesphere'] = BOOL
    DB['reflect2dskybox'] = BOOL
    DB['reflectentities'] = BOOL
    DB['reflectonlymarkedentities'] = BOOL
    DB['reflectskyboxonly'] = BOOL
    DB['rimlight'] = BOOL
    DB['rimmask'] = BOOL
    DB['scaleedgesoftnessbasedonscreenres'] = BOOL
    DB['scaleoutlinesoftnessbasedonscreenres'] = BOOL
    DB['seamless_base'] = BOOL
    DB['seamless_detail'] = BOOL
    DB['selfillumfresnel'] = BOOL
    DB['separatedetailuvs'] = BOOL
    DB['shadersrgbread360'] = BOOL
    DB['showalpha'] = BOOL
    DB['softedges'] = BOOL
    DB['spheretexkillcombo'] = BOOL
    DB['ssbump'] = BOOL
    DB['ssbumpmathfix'] = BOOL
    DB['toolmode'] = BOOL
    DB['translucentgoo'] = BOOL
    DB['unlit'] = BOOL
    DB['use_fb_texture'] = BOOL
    DB['useinstancing'] = BOOL
    DB['usingpixelshader'] = BOOL
    DB['vertexcolorlerp'] = BOOL
    DB['vertexcolormodulate'] = BOOL
    DB['vignetteenable'] = BOOL
    DB['vomitenable'] = BOOL
    DB['writez'] = BOOL
    DB['zfailenable'] = BOOL

    DB['ambientocclcolor'] = COLOR
    DB['cloakcolortint'] = COLOR
    DB['color'] = COLOR
    DB['color2'] = COLOR
    DB['colortint'] = COLOR
    DB['detailtint'] = COLOR
    DB['emissiveblendtint'] = COLOR
    DB['envmaptint'] = COLOR
    DB['fleshbordertint'] = COLOR
    DB['fleshsubsurfacetint'] = COLOR
    DB['flow_color'] = COLOR
    DB['flow_vortex_color'] = COLOR
    DB['fogcolor'] = COLOR
    DB['glassenvmaptint'] = COLOR
    DB['glowcolor'] = COLOR
    DB['layerbordertint'] = COLOR
    DB['layertint1'] = COLOR
    DB['layertint2'] = COLOR
    DB['lerpcolor1'] = COLOR
    DB['lerpcolor2'] = COLOR
    DB['light_color'] = COLOR
    DB['outlinecolor'] = COLOR
    DB['portalcolorgradientdark'] = COLOR
    DB['portalcolorgradientlight'] = COLOR
    DB['portalcoopcolorplayeroneportalone'] = COLOR
    DB['portalcoopcolorplayeroneportaltwo'] = COLOR
    DB['portalcoopcolorplayertwoportalone'] = COLOR
    DB['portalcoopcolorplayertwoportaltwo'] = COLOR
    DB['phongcolortint'] = COLOR
    DB['reflectivity'] = COLOR
    DB['reflecttint'] = COLOR
    DB['refracttint'] = COLOR
    DB['scroll1'] = COLOR
    DB['scroll2'] = COLOR
    DB['selfillumtint'] = COLOR
    DB['silhouettecolor'] = COLOR
    DB['sscolortint'] = COLOR
    DB['tint'] = COLOR
    DB['vomitcolor1'] = COLOR
    DB['vomitcolor2'] = COLOR

    DB['basetextureoffset'] = VEC2
    DB['basetexturescale'] = VEC2
    DB['bumpoffset'] = VEC2
    DB['cloudscale'] = VEC2
    DB['cropfactor'] = VEC2
    DB['emissiveblendscrollvector'] = VEC2
    DB['flowmapscrollrate'] = VEC2
    DB['magnifycenter'] = VEC2
    DB['maskscale'] = VEC2
    DB['refractionamount'] = VEC2

    DB['basealphaenvmapmaskminmaxexp'] = VEC3
    DB['bbmax'] = VEC3
    DB['bbmin'] = VEC3
    DB['dimensions'] = VEC3
    DB['entityorigin'] = VEC3
    DB['envmapfresnelminmaxexp'] = VEC3
    DB['eyeorigin'] = VEC3
    DB['eyeup'] = VEC3
    DB['flow_vortex_pos1'] = VEC3
    DB['flow_vortex_pos2'] = VEC3
    DB['forward'] = VEC3
    DB['interiorcolor'] = VEC3
    DB['leafcenter'] = VEC3
    DB['light_position'] = VEC3
    DB['phongfresnel'] = VEC3
    DB['phongfresnel2'] = VEC3
    DB['phongfresnelranges'] = VEC3
    DB['phongtint'] = VEC3
    DB['spriteorigin'] = VEC3
    DB['translucentfresnelminmaxexp'] = VEC3
    DB['uvprojoffset'] = VEC3

    DB['aainternal1'] = VEC4
    DB['aainternal2'] = VEC4
    DB['aainternal3'] = VEC4
    DB['attenfactors'] = VEC4
    DB['channel_select'] = VEC4
    DB['fadecolor'] = VEC4
    DB['flashlightcolor'] = VEC4
    DB['flesheffectcenterradius1'] = VEC4
    DB['flesheffectcenterradius2'] = VEC4
    DB['flesheffectcenterradius3'] = VEC4
    DB['flesheffectcenterradius4'] = VEC4
    DB['glintu'] = VEC4
    DB['glintv'] = VEC4
    DB['hslnoisescale'] = VEC4
    DB['irisu'] = VEC4
    DB['irisv'] = VEC4
    DB['motionblurinternal'] = VEC4
    DB['motionblurviewportinternal'] = VEC4
    DB['noisescale'] = VEC4
    DB['originfarz'] = VEC4
    DB['quatorientation'] = VEC4
    DB['scalebias'] = VEC4
    DB['selfillumfresnelminmaxexp'] = VEC4
    DB['shadowsaturationbounds'] = VEC4
    DB['uberheightwidth'] = VEC4
    DB['ubernearfar'] = VEC4
    DB['weights'] = VEC4

    DB['alternateviewmatrix'] = MATRIX
    DB['basetexturetransform'] = MATRIX
    DB['basetexturetransform2'] = MATRIX
    DB['blendmasktransform'] = MATRIX
    DB['bumptransform'] = MATRIX
    DB['bumptransform2'] = MATRIX
    DB['detail1transform'] = MATRIX
    DB['detail2transform'] = MATRIX
    DB['detailtexturetransform'] = MATRIX
    DB['detailtransform'] = MATRIX
    DB['envmapmasktransform'] = MATRIX
    DB['orientationmatrix'] = MATRIX
    DB['texture2transform'] = MATRIX
    DB['texturetransform'] = MATRIX
    DB['worldtotexture'] = MATRIX

    DB['lights'] = FOUR_CC

