

Interface to expose: 
- channels:
  - read from input channels
    - listen... type-based
    - how to route into sub-channels? 
    - refl = channel read?
  - write to output channels
    - how to write into sub-channels? 
    - add term/diff /proof
    - conflicting attempts to write to same channel
      - = sum type
      - escalate to higher scope?
  - channel is certain bitms
    - write reserves bit for certain lock period? 
    - revert constructor no longer valid when time is passed
      - remove from context
      - at time t, all rellevant bits are put to channles
  - get composed to expose
     - communication protocol
     - slam
  - session types
    - primitives are basic read/write/etc w/ composition
    - "type" - reject write if doesn't match?
  - unification?
    - more and more constraints get added? 
    - 
- how channels are variables? 
  - eliminated locally if LR and RL match R's..
    - else can be remote? Remote instance feeds in or is written to
  




Architecture: 
- Map of channels
  - id = uuid? 
  - cid if... write pointer into channel? 
    - variables = degrees of freedom (unary function = line)
  - queue of terms arrivign to global channel
    - how to get to intended sub channel? 
- Effects
  - compose channels into session types
  - capability/session type: "quoted name" -> "instance of type a"
    - can connect via local or remote? w/ same semantics? 
  - 0 does nothing
  - 1 does cut elimination (keep log/term with stamps)
    - action = just switches to 0 & adds stamps? 
- Context
  - terms (/pairs)
  - 
  
- AST
  - per node - 

- term graph 
  -       
- Equality

Steps to implement: 
- Register capabilities
  - "1" capability
   - 0:"1" on left -- declares capability
   - 1:<info> on right.. allows executing capability
- as type

