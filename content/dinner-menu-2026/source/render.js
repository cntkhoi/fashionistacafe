const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const [bleed,out]=[process.argv[2]==='1',process.argv[3]];
await p.goto('file://'+__dirname+'/menu.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
if(bleed)await p.evaluate(()=>document.body.classList.add('bleed'));
const w=bleed?'136mm':'130mm',h=bleed?'216mm':'210mm';
await p.pdf({path:out,width:w,height:h,printBackground:true,margin:{top:0,left:0,right:0,bottom:0}});
await b.close()})()
