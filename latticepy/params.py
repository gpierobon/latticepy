
switch = False

# This allows to run the simulation like this
# python3 main.py $NDIMS $N $DEV ...
if switch == True:
    '''
    NDIMS     = int(sys.argv[1]) 
    N         = int(sys.argv[2])
    DEV       = sys.argv[3]
    PREC      = sys.argv[4]
    VERB      = sys.argv[5]
    ICTYPE    = sys.argv[]
    ICFILE    = sys.argv[]
    L         = float(sys.argv[])
    dt        = float(sys.argv[])
    t         = float(sys.argv[])
    tf        = float(sys.argv[])
    G         = float(sys.argv[])
    '''
else:
    NDIMS     = 3                         # Grid dimension
    N         = 256                       # Grid size
    DEV       = 'gpu'                     # Device to use ('cpu' or 'gpu')
    PREC      = 'single'                  # Floating point precision ('single' or 'double')
    VERB      = 'normal'                  # Verbosity in the printing outputs ('silent' or 'normal')
    ICTYPE    = 'solitons'                # Initial conditions type ('solitons' or ...)
    ICFILE    = 'solitons.txt'            # File to read in IC if applicable
    L         = 1                         # Box size in physical coordinates
    REFR      = 'MRE'                     # Hubble expansion ('MRE' or 'RD' or 'MD' or 'static')
    dt        = L/N/4.                    # Timestep
    t         = 0                         # Initial time 
    tf        = 0.5                       # Final time
    G         = 4000                      # Newton's constant   
