import{_ as g}from"./CsvTable-CfwIKEBv.js";import{_ as c}from"./slidev/CodeBlockWrapper.vue_vue_type_script_setup_true_lang-ByxWBMfz.js";import{_ as y}from"./StickyNote-xApWLbeV.js";import{D as _,b as n,o as e,w as l,g as s,e as r,m as u,B as i,E as C,v as D,x as f,C as k}from"./modules/vue-iF0bmrqZ.js";import{_ as F}from"./2_68_sql_dml2-8-BXU8UnXZ.js";import{I as x}from"./two-cols-title-Cs8AM-lr.js";import{u as v,f as A}from"./slidev/context-DcSgYnU8.js";import"./modules/unplugin-icons-DnuKfxKQ.js";import"./index-BZ38dv6p.js";import"./modules/shiki-BP1AGWD6.js";import"./slidev/TitleIcon.vue_vue_type_script_setup_true_lang-5GxsMunJ.js";const T={class:"flex gap-2"},b={class:"w-1/2"},W={__name:"sql_dml2.md__slidev_105",setup(w){const{$clicksContext:h,$frontmatter:o}=v();return h.setup(),(B,t)=>{const p=y,d=c,E=g,m=_("drag");return e(),n(x,D(f(k(A)(k(o),104))),{title:l(a=>[t[1]||(t[1]=s("p",null,[s("span",{class:"text-2xl"},"WITH Clause")],-1)),t[2]||(t[2]=s("ul",null,[s("li",null,[s("code",null,"CTE"),i(" : For show order details of high order")])],-1)),C((e(),n(p,{color:"amber-light",textAlign:"left",width:"180px",title:"Note",markdownSource:[5,6,76]},{default:l(()=>[...t[0]||(t[0]=[i(" Common Table Expressions (CTE) ",-1)])]),_:1})),[[m,[477,54,241,62]]])]),left:l(a=>[r(d,u({},{title:"",ranges:[]}),{default:l(()=>[...t[3]||(t[3]=[s("pre",{class:"shiki shiki-themes slack-dark snazzy-light slidev-code",style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869","--shiki-dark-bg":"#222222","--shiki-light-bg":"#FAFBFC"}},[s("code",{class:"language-sql"},[s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"WITH")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"    cte_order "),s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"AS"),s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}}," (")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"        SELECT")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"            orderNumber,")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#DCDCAA","--shiki-light":"#09A1ED"}},"            COUNT"),s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"(orderNumber) "),s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"AS"),s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}}," items")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"        FROM")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"            orderdetails")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"        GROUP BY")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"            orderNumber")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"    )")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"SELECT")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#D4D4D4","--shiki-light":"#ADB1C2"}},"    *")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"FROM")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"    cte_order")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"where")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#2DAE58"}},"    cte_order"),s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"."),s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#2DAE58"}},"items"),s("span",{style:{"--shiki-dark":"#D4D4D4","--shiki-light":"#ADB1C2"}}," ="),s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}}," (")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"        select")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#DCDCAA","--shiki-light":"#09A1ED"}},"            max"),s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"(items)")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#569CD6","--shiki-light":"#11658F"}},"        from")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"            cte_order")]),i(`
`),s("span",{class:"line"},[s("span",{style:{"--shiki-dark":"#E6E6E6","--shiki-light":"#565869"}},"    );")])])],-1)])]),_:1},16)]),right:l(a=>[s("div",T,[s("div",b,[r(E,null,{default:l(()=>[...t[4]||(t[4]=[s("pre",null,`"ordernumber"	"items"
10168	18
10332	18
10316	18
10398	18
10360	18
10159	18
10165	18
10386	18
10106	18
10275	18
10222	18
`,-1)])]),_:1})]),t[5]||(t[5]=s("div",{class:"w-1/2"},[s("div",{class:"w-fit mx-auto"},[s("p",null,[s("img",{src:F,alt:"2_68_sql_dml2-8",class:"max-h-50vh"})])])],-1))])]),default:l(a=>[...t[6]||(t[6]=[])]),_:1},16)}}};export{W as default};
