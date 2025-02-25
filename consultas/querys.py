def consultAsociado(cedula):
  return f"""
    Select gr001.N_NOMBR1 p_nombre, gr001.N_NOMBR2 s_nombre, gr001.N_APELL1 p_apellido, gr001.N_APELL2 s_apellido, 
        DECODE(GR001.I_IDETER, 'A', 'NIT',
                                    'C', 'Cédula',
                                    'O', 'Otros',
                                    'E', 'Cédula_Extranjeria',
                                    'T', 'Tarjeta_Identidad',
                                    'P', 'Pasaporte',
                                    '', ' ') TIPO_DOCUMENTO,
        gr001.A_NUMNIT Numero_Idenitificacion, 
        gr005c.T_TERCEL Celular_corres,
        gr005c.D_TERCER Direccion_corres,
        gr005c.n_barrio Barrio_corres,
        ubica_2.n_ciudad Ciudad_corres,
        ubica_2.n_depart Departamento_corres,
        gr005c.D_EMAIL Email_corres,
        gr1067.I_CTAEXT Cuentas_exterior
        from GR001MTERCERO gr001, GR582DACTXTERC gr582, GR581TACTIVECO gr581, CM120MPROVEEDO cm120, AP014MCLIENTE ap014,
        GR005MDIRECCIO gr005c, GR005MDIRECCIO gr005r,GR1067MDATTERC gr1067, NO223MEMPLEADO no223, GR815MPROFESIO gr815,
        (select ap72.K_IDTERC, sum(ap72.V_COMERC) v_comerc from AP792DACTIVXCL ap72 group by ap72.K_IDTERC) ap792, 
        (select ap73.K_IDTERC, sum(ap73.V_saldo) v_saldo from AP793DPASIVXCL ap73 group by ap73.K_IDTERC) ap793, 
        (Select max (ca67.k_numdoc),ca67.K_IDTERC, sum(ca67.V_COMERC) V_COMERC from CA657DACTXSOL ca67 group by CA67.K_IDTERC) ca657, 
        (Select max (ca68.k_numdoc),ca68.K_IDTERC, sum(ca68.V_SALDO) V_SALDO from CA658DPASXSOL ca68 group by ca68.K_IDTERC) ca658,
        (SELECT AP83.K_IDTERC, SUM(AP83.V_DEVENG) V_DEVENG FROM AP783GINGREEGR AP83 WHERE AP83.K_CONCPG IN ('001','002','201','202','401','003') GROUP BY AP83.K_IDTERC) AP783_1,
        (SELECT AP73.K_IDTERC, SUM(AP73.V_DEDUCE) V_DEDUCE FROM AP783GINGREEGR AP73 WHERE AP73.K_CONCPG IN ('101','102','301','302','050','052','303','051') GROUP BY AP73.K_IDTERC) AP783_2,
        (Select gr002.K_CIUDAD, gr002.N_CIUDAD, gr002.K_DEPART, gr003.N_DEPART, gr002.K_PAIS, gr004.N_PAIS from GR002MCIUDAD gr002, GR003MDEPARTAM gr003, GR004MPAIS gr004
        Where gr002.K_DEPART = gr003.K_DEPART
        and gr002.K_PAIS = gr004.K_PAIS
        and gr003.K_PAIS = gr004.K_PAIS) ubica_1,
        (Select gr002.K_CIUDAD, gr002.N_CIUDAD, gr002.K_DEPART, gr003.N_DEPART, gr002.K_PAIS, gr004.N_PAIS from GR002MCIUDAD gr002, GR003MDEPARTAM gr003, GR004MPAIS gr004
        Where gr002.K_DEPART = gr003.K_DEPART
        and gr002.K_PAIS = gr004.K_PAIS
        and gr003.K_PAIS = gr004.K_PAIS) ubica_2,
        (Select gr002.K_CIUDAD, gr002.N_CIUDAD, gr002.K_DEPART, gr003.N_DEPART, gr002.K_PAIS, gr004.N_PAIS from GR002MCIUDAD gr002, GR003MDEPARTAM gr003, GR004MPAIS gr004
        Where gr002.K_DEPART = gr003.K_DEPART
        and gr002.K_PAIS = gr004.K_PAIS
        and gr003.K_PAIS = gr004.K_PAIS) ubica_3,
        (Select gr001.k_idterc, max (gr001.F_MOVIM_ADT) F_MOVIM_ADT from lnxadt.gr001mauditar gr001 group by gr001.k_idterc order by gr001.k_idterc desc) gr001aud,
        (Select ap014.k_idterc, max (ap014.F_MOVIM_ADT) F_MOVIM_ADT from lnxadt.ap014mauditar ap014 group by ap014.k_idterc order by ap014.k_idterc desc) ap014aud,
        (Select cm120.k_idterc, max (cm120.F_MOVIM_ADT) F_MOVIM_ADT from lnxadt.cm120mauditar cm120 group by cm120.k_idterc order by cm120.k_idterc desc) cm120aud
        Where gr001.K_IDTERC = gr582.K_IDTERC (+)
        and AP014.K_IDTERC (+) = GR001.K_IDTERC
        and ap014.aanumnit = '{cedula}'
        and CM120.K_IDTERC (+) = GR001.K_IDTERC
        and gr582.K_ACTIVI = gr581.K_ACTIVI (+)
        and ap792.K_IDTERC (+) = gr001.K_IDTERC
        and ap793.K_IDTERC (+) = gr001.K_IDTERC
        and ca657.K_IDTERC (+) = gr001.K_IDTERC
        and ca658.K_IDTERC (+) = gr001.K_IDTERC
        AND AP783_1.K_IDTERC (+) = GR001.K_IDTERC
        AND AP783_2.K_IDTERC (+) = GR001.K_IDTERC
        anD NO223.K_IDTERC (+) = GR001.K_IDTERC
        and gr005c.I_TIPDIR (+) = 'C' 
        and gr005r.I_TIPDIR (+) = 'R' 
        and gr005c.K_IDTERC (+) = gr001.K_IDTERC
        and gr005R.K_IDTERC (+) = gr001.K_IDTERC
        and gr1067.K_IDTERC (+) = gr001.K_IDTERC
        and gr815.K_PROFES (+) = gr001.K_PROFES
        and ubica_1.k_ciudad (+) = gr001.K_CIUDAD_IDE
        and ubica_1.k_pais (+) = gr001.K_PAIS_IDE
        and ubica_2.k_ciudad (+) = gr005c.K_CIUDAD
        and ubica_2.K_DEPART (+) = gr005c.K_DEPART
        and ubica_3.k_ciudad (+) = ap014.K_CIUDAD_NAC
        and ubica_3.K_DEPART (+) = ap014.K_DEPART_NAC
        and ap014aud.k_idterc (+) = gr001.k_idterc
        and gr001aud.k_idterc (+) = gr001.K_IDTERC
        and cm120aud.k_idterc (+) = gr001.K_IDTERC
        and ap014.I_ESTASO = 'A'
        order by gr001.A_NUMNIT
        """