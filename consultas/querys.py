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