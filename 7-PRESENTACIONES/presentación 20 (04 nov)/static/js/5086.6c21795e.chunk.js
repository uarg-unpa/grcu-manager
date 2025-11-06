"use strict";(self.webpackChunk_genially_view_client=self.webpackChunk_genially_view_client||[]).push([[5086],{89690:(e,t,n)=>{n.d(t,{Z:()=>a});var i=n(45992),r=n(13847),o=n(11833);const a=e=>{let{title:t,frontImageSrc:n,coverImageSrc:a,fitImages:s,flipped:l,burned:d,onClick:u}=e;const c=Boolean(d),m=Boolean(l);return(0,i.jsxs)(o.Ox,{role:"button",$burned:c,$flipped:m,onClick:e=>{e.stopPropagation(),u&&u()},"aria-label":`Card showing ${m?"front":"back"} side with title: ${t}`,"aria-disabled":c,tabIndex:c?-1:0,children:[(0,i.jsx)("img",{style:{opacity:m?1:0,position:"absolute",top:0,left:0,width:"100%",height:"100%",objectFit:s?"contain":"cover",transition:`opacity ${o.uD}ms steps(1)`},src:n,alt:"front"}),(0,i.jsx)("img",{style:{opacity:m?0:1,position:"absolute",top:0,left:0,width:"100%",height:"100%",objectFit:s?"contain":"cover",transition:`opacity ${o.uD}ms steps(1)`},src:a,alt:"cover"}),t&&(0,i.jsx)(o.aW,{hidden:!m,children:(0,i.jsx)(r.m_,{text:t,placement:r.m_.Position.TOP,fallbackPlacements:[r.m_.Position.TOP],renderReferencePortalNode:document.querySelector("body"),children:(0,i.jsx)(o.hE,{"data-testid":"card-title",children:t})})})]})}},11833:(e,t,n)=>{n.d(t,{Ox:()=>l,aW:()=>a,hE:()=>s,rl:()=>r,uD:()=>o});var i=n(37577);const r=1e3,o=r/3.4,a=i.Ay.div({display:"flex",justifyContent:"center",alignItems:"center",flexShrink:0,position:"absolute",paddingLeft:"12px",paddingRight:"12px",bottom:0,left:0,userSelect:"none",minHeight:"25%",top:"75%",width:"100%",backgroundColor:"rgba(18,18,18,0.5)"}),s=i.Ay.p({color:"white",fontSize:12,textAlign:"center",fontStyle:"normal",fontWeight:400,lineHeight:"16px",overflow:"hidden",textOverflow:"ellipsis",wordWrap:"break-word",whiteSpace:"nowrap",pointerEvents:"none"}),l=i.Ay.div`
  @keyframes rotate-out {
    0% {
      transform: rotateY(0deg);
    }
    33% {
      transform: rotateY(90deg);
    }
    100% {
      transform: rotateY(0deg);
    }
  }

  @keyframes rotate-in {
    0% {
      transform: rotateY(0deg);
    }
    33% {
      transform: rotateY(90deg);
    }
    100% {
      transform: rotateY(0deg);
    }
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
    }
    12% {
      transform: scale(1.05, 1.05);
    }
    40% {
      transform: scale(1.05, 1.05);
    }
    100% {
      transform: scale(1);
    }
  }

  position: relative;
  overflow: hidden;
  flex-shrink: 0;
  width: 100%;
  height: 100%;
  container-type: size;

  cursor: ${e=>{let{$flipped:t,$burned:n}=e;return t||n?"default":"pointer"}};

  animation-name: ${e=>{let{$flipped:t}=e;return t?"rotate-out":"rotate-in"}}
    ${e=>{let{$burned:t}=e;return t?",pulse":""}};
  animation-duration: ${r}ms;
  animation-delay: 0ms, ${r}ms;
  animation-iteration-count: 1;
  animation-timing-function: ease-out, ease-in-out;
  perspective: 1500px;

  border-radius: 9%;
  @supports (container-type: size) {
    border-radius: 6cqmin;
  }

  /* HACK: We need to set border as important because .genially-embed is reseting our borders in the View */
  border: 1px solid
    ${e=>{let{theme:t,$flipped:n}=e;return n?t.color.border.primary.disabled():t.color.border.primary.default()}} !important;
  outline: 1px white solid;

  filter: ${e=>{let{$flipped:t}=e;return t?"":"drop-shadow(0px 1px 4px rgba(0, 15, 51, 0.2))"}};

  &:hover {
    filter: ${e=>{let{$flipped:t}=e;return t?"":"drop-shadow(rgba(0, 15, 51, 0.3) 0px 1px 8px)"}};
    border-color: ${e=>{let{theme:t,$flipped:n}=e;return n?t.color.border.primary.disabled():t.color.border.primary.hover()}} !important;
  }

  ${a} {
    visibility: ${e=>{let{$flipped:t}=e;return t?"initial":"hidden"}};
    transition: visibility ${o}ms steps(1);
    z-index: 1;
  }

  &:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    z-index: 2;
    width: 100%;
    height: 100%;
    opacity: ${e=>{let{$burned:t}=e;return t?"0.4":"0"}};
    transition: opacity ${r}ms steps(1);
    transition-delay: ${r}ms;
    background-color: white;
    pointer-events: none;
  }
`},56292:(e,t,n)=>{n.d(t,{x:()=>u});var i=n(45992),r=n(40671),o=n(99049),a=n(76838),s=n(37577);const l=s.Ay.div`
  container-type: size;
  height: 100%;
  padding: 8px;
`,d=s.Ay.div`
  --contained-gap: 16px;

  display: grid;
  grid-template-columns: repeat(${e=>e.numColumns}, minmax(0, 1fr));
  grid-template-rows: repeat(${e=>e.numRows}, 1fr);
  grid-auto-flow: column;
  height: 100%;
  gap: var(--contained-gap);

  @supports (container-type: size) {
    --contained-gap: 4cqmin;
  }
`,u=(s.Ay.canvas({width:"100%",height:"100%",pointerEvents:"none",position:"absolute",top:0,left:0,zIndex:3}),e=>{let{items:t,renderItem:n,keyExtractor:s,getComputedStyles:u,forcedRows:c}=e;const m=(0,a.f)(t.length,c);return(0,i.jsx)(l,{children:(0,i.jsx)(d,{numColumns:m.numColumns,numRows:m.numRows,children:(0,i.jsx)(r.N,{children:t.map(((e,t)=>(0,i.jsx)(o.P.div,{layout:!0,style:u?u(e,t):void 0,initial:{opacity:0,scale:.7},animate:{opacity:1,scale:1},transition:{type:"spring",ease:"easeInOut",stiffness:30,damping:10},"data-testid":`grid-item-${s(e)}`,children:n(e)},s(e))))})})})})},30555:(e,t,n)=>{n.d(t,{B:()=>o,u:()=>s});var i=n(54072);const r=e=>null!==e,o=e=>{if(e&&"action"in e){const{action:t}=e;return t&&"source"in t&&t.source?t.source:""}if(e&&"data"in e){const{data:t}=e;return t&&"source"in t&&t.source?t.source:""}return""},a=(e,t)=>{var n;const i=null===(n=e.image)||void 0===n?void 0:n.source,r=o(e.audio);return i?{id:t,src:i,title:e.title,altText:e.image.altText||"",audioSource:r}:null},s=function(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];return e.flatMap((e=>{const n=(0,i.Ak)(),r=a(e,`${n}-original`),s=t?a(e,`${n}-pair`):((e,t)=>{var n,i;const r=null===(n=e.imagePair)||void 0===n?void 0:n.source;if(!r)return null;const a=o(e.audioPair);return{id:t,src:r,title:e.titlePair||e.title,altText:(null===(i=e.imagePair)||void 0===i?void 0:i.altText)||"",audioSource:a}})(e,`${n}-pair`);return[r,s]})).filter(r)}},76838:(e,t,n)=>{n.d(t,{f:()=>r,v:()=>i});const i=e=>{if("auto"===e)return;const t=Number(e);if(!Number.isNaN(t))return t;console.warn("Cannot parse row distribution. Setting to auto",e)},r=(e,t)=>t?((e,t)=>e<t?{numColumns:1,numRows:e}:{numColumns:Math.ceil(e/t),numRows:t})(e,t):(e=>{if(e<4)return{numColumns:1,numRows:e};let t=4;for(;e%t!==0&&t<7;)t+=1;return{numColumns:t,numRows:Math.ceil(e/t)}})(e)},22705:(e,t,n)=>{n.r(t),n.d(t,{geniallyFindThePairViewScript:()=>E});var i=n(45992),r=n(10285),o=n(84054),a=n(60708),s=n(41381),l=n(17588),d=n(37577),u=n(89690),c=n(56292),m=n(50414);var p;!function(e){e.FACEDOWN="faceDown",e.FACEUP="faceUp",e.BURNED="burned"}(p||(p={}));const f=e=>e.replace("-original","-pair");var g=n(11833);const h=(e,t)=>{const n=e%2===1,i=t%2===1;return n&&!i?1:!n&&i?-1:e-t},b=e=>{let{theme:t,images:n,coverImageSrc:r,fitImages:o,rowsDitributionFromConfig:a,onSuccess:s,onFailure:b,onGameWon:v,onFaceUp:y}=e;const{shuffledCards:w,isFaceUp:x,isBurned:E,onPick:C}=((e,t,n,i,r)=>{const o=(0,l.useMemo)((()=>{const t=e.map((e=>{return Object.assign(Object.assign({},e),{id:e.id,pairId:e.id.includes("-pair")?(t=e.id,t.replace("-pair","-original")):f(e.id)});var t}));return(0,m.U)(t)}),[e]),[a,s]=(0,l.useState)((()=>{const e=new Map;return o.forEach((t=>{e.set(t.id,{id:t.id,status:p.FACEDOWN,pairId:t.pairId})})),e})),d=(0,l.useCallback)((e=>{var t;return(null===(t=a.get(e))||void 0===t?void 0:t.status)===p.FACEUP}),[a]),u=(0,l.useCallback)((e=>{var t;return(null===(t=a.get(e))||void 0===t?void 0:t.status)===p.BURNED}),[a]);return{shuffledCards:o,isFaceUp:d,isBurned:u,onPick:e=>{const o=a.get(e);if(o.status!==p.FACEDOWN)return;const l=[...a.values()].filter((e=>e.status===p.FACEUP));if(0===l.length)a.set(o.id,Object.assign(Object.assign({},o),{status:p.FACEUP}));else if(1===l.length){const e=l[0];e.pairId===o.id?(a.set(e.id,Object.assign(Object.assign({},e),{status:p.BURNED})),a.set(o.id,Object.assign(Object.assign({},o),{status:p.BURNED})),t()):(a.set(o.id,Object.assign(Object.assign({},o),{status:p.FACEUP})),n())}else 2===l.length&&(l.forEach((e=>{a.set(e.id,Object.assign(Object.assign({},e),{status:p.FACEDOWN}))})),a.set(o.id,Object.assign(Object.assign({},o),{status:p.FACEUP})));r(o.id),s(new Map(a)),[...a.values()].every((e=>e.status===p.BURNED))&&i()}}})(n,(()=>{setTimeout((()=>{s()}),g.rl)}),(()=>{setTimeout((()=>{b()}),g.rl)}),(()=>{setTimeout((()=>{v()}),g.rl)}),(e=>{y(e)})),[S,$]=(0,l.useState)((()=>Array.from({length:w.length},((e,t)=>t))));return(0,l.useEffect)((()=>{$((e=>[...e].sort(h).reverse()))}),[]),(0,i.jsx)(d.NP,{theme:t,children:(0,i.jsx)(c.x,{items:w,forcedRows:a,renderItem:e=>(0,i.jsx)(u.Z,{title:e.title,frontImageSrc:e.src,coverImageSrc:r,fitImages:o,flipped:x(e.id)||E(e.id),burned:E(e.id),onClick:()=>C(e.id)}),keyExtractor:e=>e.id,getComputedStyles:(e,t)=>({order:S[t]})})})};var v=n(30555),y=n(76838);const w="https://audios.genial.ly/59e059d30b9c21060cb4c2ec/de8b3efe-c4df-48ff-8bbb-2b3e940663d3.wav",x="https://audios.genial.ly/59e059d30b9c21060cb4c2ec/23fe908b-44e2-4972-981f-d857c429b126.wav",E=(e,t)=>{e.slide.audioRequirement=o.w.ShowMute;const n=e.config.itemList,l=(0,v.u)(n,e.config.identicalImages);(0,s.p)({getTargetNodeItem:()=>e.item,initialState:{hasSlideEntered:!1},renderApp:n=>{let{setState:o}=n;var s;const{coverImage:d,fitImages:u,numRows:c,onEndAction:m}=e.config,p=e.item;t.preloadAudio(w),t.preloadAudio(x),l.forEach((e=>{t.preloadAudio(e.audioSource)}));const f=()=>{t.playAudio({source:w})},g=()=>{t.playAudio({source:x})},h=()=>{null===m||void 0===m||m.run()};return null===(s=null===p||void 0===p?void 0:p.parentSlide)||void 0===s||s.on(a.m.Entered,(()=>{o({hasSlideEntered:!0})})),e=>{let{hasSlideEntered:n=!1}=e;if(!n)return(0,i.jsx)(i.Fragment,{});const o=[];return(0,i.jsx)(b,{theme:t.theme,images:l,coverImageSrc:String(d.source),fitImages:u,rowsDitributionFromConfig:(0,y.v)(c),onSuccess:f,onFailure:g,onGameWon:h,onFaceUp:e=>{const n=l.find((t=>t.id===e));if(!n||!n.audioSource)return;o.forEach((e=>{t.playAudio(Object.assign(Object.assign({},e),{playMode:r.F.Stop}))})),o.length=0;const i={source:n.audioSource,playMode:r.F.PlayRestart},a=t.playAudio(i);o.push(Object.assign(Object.assign({},i),{refId:a.refId}))}})}}})(e,t)}},41381:(e,t,n)=>{n.d(t,{p:()=>a});var i=n(70377),r=n(66264),o=n(60708);function a(e){let{getTargetNodeItem:t,renderApp:n,renderThumbnailApp:a,initialState:s}=e,l=!1;const d=[],u=e=>{d.push(e)};return e=>{const c=t(e.config),m=null===c||void 0===c?void 0:c.parentSlide;function p(){if(!c)return;let e=null;if("idOfFreeNode"in c)e=document.getElementById(c.idOfFreeNode);else{const t=document.createElement("div");t.innerHTML=c.source;let n=t.getElementsByClassName("genially-widget-app");n.length||(n=t.getElementsByClassName("genially-widget-gallery"));const{id:i}=n[0];if(!i)return;e=document.getElementById(i)}if(e){const t=r=>{if(l){const o=n({setState:t,onUnmount:u});i.render(o(r),e)}else console.warn('"rerender" was called when the widget was already unmounted. This is a no-op. Did you forget to dispose of an event handler with "onUnmount"?')};l=!0,t(s),d.push((()=>{i.unmountComponentAtNode(e)}))}}function f(){l=!1,d.forEach((e=>{e()})),d.length=0}c&&"isTransversal"in c&&c.isTransversal?(null===c||void 0===c||c.on(r.q.Mount,(()=>{p()})),null===c||void 0===c||c.on(r.q.Unmount,(()=>{f()}))):(null===m||void 0===m||m.on(o.m.Entering,(()=>{l||p()})),null===m||void 0===m||m.on(o.m.Exited,(()=>{l&&f()}))),null===m||void 0===m||m.on(o.m.ThumbnailMount,(()=>{!function(){if(!a||!c||!("idOfThumbnailFreeNode"in c))return;const e=document.getElementsByClassName(c.idOfThumbnailFreeNode);Array.from(e).forEach((e=>{i.unmountComponentAtNode(e)}))}(),function(){if(!a||!c||!("idOfThumbnailFreeNode"in c))return;const e=document.getElementsByClassName(c.idOfThumbnailFreeNode);Array.from(e).forEach((e=>{i.render(a(),e)}))}()}))}}}}]);
//# sourceMappingURL=https://s3-static-genially.genially.com/view/static/js/5086.6c21795e.chunk.js.map