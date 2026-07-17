RELATION_PROMPT = """
Extract relationships.

Return JSON only.

Example

{
 "relationships":[
   {
     "source":"Pump P-101",
     "relation":"CONNECTED_TO",
     "target":"Valve V-11"
   }
 ]
}

Document

{text}
"""