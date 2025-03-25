def consultAsociado(cedula):
  return f"""
    Select gr001.N_NOMBR1 ||' '|| gr001.N_NOMBR2 ||' '|| gr001.N_APELL1 ||' '|| gr001.N_APELL2 ||' '|| GR001.N_RAZONS Nombre, 
        gr001.A_NUMNIT Idenitificacion, 
        gr005c.T_TERCEL Celular,
        gr005c.T_TERcer Fijo,
        gr005c.D_TERCER Direccion,
        gr005c.D_EMAIL Email,
        AP014.I_ESTASO Asociado
        from GR001MTERCERO gr001, AP014MCLIENTE ap014,
        GR005MDIRECCIO gr005c         
        Where AP014.K_IDTERC (+) = GR001.K_IDTERC
        and ap014.aanumnit = '{cedula}'
        and gr005c.I_TIPDIR (+) = 'C' 
        and gr005c.K_IDTERC (+) = gr001.K_IDTERC       
        order by gr001.A_NUMNIT
        """


def consultPagaduria():
  return f"""
    select ASOCIADOS.k_Nomina, count (ASOCIADOS.AANUMNIT) Num_Asociados, count (CDT.AANUMNIT) NUM_CDAT, count (COOVIAHORRO.AANUMNIT) NUM_COOVIAHORO, count (CARTERA.AANUMNIT) NUM_CREDITOS, count (HVISTA.AANUMNIT) NUM_HVISTA
      FROM 
      (SELECT aP014.AANUMNIT, count(dr041.k_tipodr || dr041.k_numdoc) Num_prod, AP014.K_NOMINA
      FROM AP014MCLIENTE AP014, dr041mgdocumen dr041
      WHERE DR041.K_IDTERC = AP014.K_IDTERC AND  dr041.k_tipodr IN
                  ('3') AND pk_dr_vencimiento.fu_v_saldo_documento (dr041.k_tipodr,dr041.k_numdoc,SYSDATE) > 0 
                  and ap014.I_ESTASO = 'A'
      GROUP BY AP014.AANUMNIT, AP014.K_NOMINA) ASOCIADOS,


      (SELECT aP014.AANUMNIT, count(CD387.V_TITULO) Cant_TITULOs, AP014.K_NOMINA 
      FROM AP014MCLIENTE AP014, CD387mcertidep cd387 
      WHERE CD387.K_IDTERC = AP014.K_IDTERC AND  cd387.i_estado IN ('C')
      GROUP BY AP014.AANUMNIT, AP014.K_NOMINA, AP014.K_NOMINA) CDT,

      (SELECT aP014.AANUMNIT, count(dr041.k_tipodr ||dr041.k_numdoc) Num_prod, DR041.K_NOMINA 
      FROM AP014MCLIENTE AP014, dr041mgdocumen dr041
      WHERE DR041.K_IDTERC = AP014.K_IDTERC AND  dr041.k_tipodr IN
                  ('27', '30', '47', '100', '101', '102', '103', '104', '105',
                    '106', '107', '108', '109', '110', '111', '57', '60', '61',
                    '62') AND pk_dr_vencimiento.fu_v_saldo_documento (dr041.k_tipodr,
                                                        dr041.k_numdoc,
                                                        SYSDATE
                                                      ) > 0 
      GROUP BY AP014.AANUMNIT, DR041.K_NOMINA) COOVIAHORRO,


      (SELECT aP014.AANUMNIT, count( ca090.a_tipodr ||ca090.a_obliga) num_creditos, ca090.K_NOMINA Nom_Cartera
      FROM AP014MCLIENTE AP014, ca090mgsolcred ca090
      WHERE ca090.K_IDTERC = AP014.K_IDTERC AND ca090.i_estsol = 'C'
          AND ca090.i_cancel <> 'H'
                    AND pk_ca_funcion.fu_concepto ('CAPITAL',
                                                    'SALDO',
                                                    ca090.a_tipodr,
                                                    ca090.a_obliga,
                                                    SYSDATE,
                                                    'TRUE',
                                                    'T'
                                                  ) > 0
      GROUP BY AP014.AANUMNIT, ca090.K_NOMINA) CARTERA,

      (SELECT aP014.AANUMNIT,count(ah136.k_cuenta) Num_cun_ahoro, AP014.K_NOMINA
      FROM AP014MCLIENTE AP014, ah136mcuenta ah136
      WHERE ah136.K_IDTERC_aso = AP014.K_IDTERC 
                    AND pk_ah_saldo.fu_v_saldo_actual_dia (ah136.k_cuenta,
                                                  '21050501',
                                                  ah136.k_sucurs,
                                                  SYSDATE
                                                  ) > 0
      GROUP BY AP014.AANUMNIT, AP014.K_NOMINA) HVISTA
      WHERE 
      ASOCIADOS.AANUMNIT = CDT.AANUMNIT (+)
      AND ASOCIADOS.AANUMNIT = COOVIAHORRO.AANUMNIT (+)
      AND ASOCIADOS.AANUMNIT = CARTERA.AANUMNIT (+)
      AND ASOCIADOS.AANUMNIT = HVISTA.AANUMNIT (+)
      --AND ASOCIADOS.K_NOMINA = '4'
      GROUP BY ASOCIADOS.k_Nomina
    """

def infoPagaduria():
  return f"""
    select ap016.K_NOMINA, ap016.N_NOMINA, gr001.A_NUMNIT, gr001.N_RAZONS, AP016.F_MOVIM_ADT F_CREACION, GR001.N_SIGLA SIGLA, GR001.K_TIPOEM, gr001.K_PAIS_IDE, gr001.K_DEPART_IDE, gr001.K_CIUDAD_IDE, gr001.O_NUMNIT_REP, gr001.N_REPLEG 
    from gr001mtercero gr001, ap016mdefnomin ap016
    where gr001.k_idterc = ap016.K_IDTERC
  """