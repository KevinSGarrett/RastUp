---
id: TD-408
title: "**1.20.D Optional native shells (React Native + Expo)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-408-120d-optional-native-shells-react-native-expo\TD-408-overview.md"
parent_id: 
anchor: "TD-408"
checksum: "sha256:39a6f0d8a58b02c387bb13158607dab07d1062e09ef56fea91ff9179fe203aa0"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-408"></a>
## **1.20.D Optional native shells (React Native + Expo)**

**Project layout**  
**Recommended path:** *apps/mobile/App.tsx*

*export default function App() {*  
*return (*  
*\<SafeAreaProvider\>*  
*\<NavigationContainer linking={linking}\>*  
*\<Stack.Navigator\>*  
*\<Stack.Screen name="Home" component={HomeScreen}/\>*  
*\<Stack.Screen name="Messages" component={MessagesScreen}/\>*  
*\<Stack.Screen name="Booking" component={BookingScreen}/\>*  
*\<Stack.Screen name="Web" component={WebViewScreen}/\> {/\* for hybrid routes if needed \*/}*  
*\</Stack.Navigator\>*  
*\</NavigationContainer\>*  
*\</SafeAreaProvider\>*  
*);*  
*}*  

**Deep link config**  
**Recommended path:** *apps/mobile/linking.ts*

*export default {*  
*prefixes: \['rastup://','https://rastup.com'\],*  
*config: { screens: {*  
*Home: '',*  
*Messages: 'messages',*  
*Booking: 'checkout/:id',*  
*Profile: 'p/:handle',*  
*Studio: 's/:slug'*  
*}}*  
*};*  

**Platform considerations (high‑level policy):** at launch, **PWA can be primary**. If/when we publish native apps, limit the initial native scope to discovery, booking, messages, and studios; keep **Fan‑Sub paid content flows** in the web experience until we explicitly decide to support native in‑app purchase workflows.
