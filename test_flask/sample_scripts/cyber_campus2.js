function top2menuView(a){ //2차메뉴보기
  if(this.id){
    eidStr = this.id;
    var _$aa = eidStr.lastIndexOf("m",eidStr.length)+1;
    eidNum=eidStr.substring(_$aa,eidStr.length);
    a = parseInt(eidNum);
  }
  top2menuHideAll();
  top1Menu = document.getElementById("top1m"+a);
  top2Menu = document.getElementById("top2m"+a);
  ann=a;
  if (a=0) { //메인은2차메뉴활성화안함
  } else {
    if (top1Menu) {
      top1Menu.firstChild.className = "site-background-color";
      if (top2Menu) { top2Menu.style.display = 'inline'; }
    }
  }
}

function top2menuHide(a){ //2차메뉴감추기
  if(this.id && a != 1){
    eidStr = this.id;
    var _$aa = eidStr.lastIndexOf("m",eidStr.length)+1;
    eidNum=eidStr.substring( _$aa,eidStr.length);
    a = parseInt(eidNum);
  }
  top2menuHideAll();
  top1Menu = document.getElementById("top1m"+a);
  top2Menu = document.getElementById("top2m"+a);
  top1MenuCurr = document.getElementById("top1m0");
  top2MenuCurr = document.getElementById("top2m0");
  //if(a<10){ann='0'+a;} else {ann=''+a;}
  ann=a;
  if (top1Menu) {
    top1Menu.firstChild.className = "gnb-top-class-off";
    if (top2Menu) { top2Menu.style.display = 'none'; }
    if (top1MenuCurr) { 
      }
    if (top2MenuCurr) { top2MenuCurr.style.display = 'inline'; }
  }
}

function top2menuHideAll(){ //2차메뉴모두감추기
  top1menuEl = document.getElementById("top1menu").getElementsByTagName("ul");
  for (i=1;i<=top1menuEl.length;i++){
    top1Menu = document.getElementById("top1m"+i);
    top2Menu = document.getElementById("top2m"+i);
    //if(i<10){inn='0'+i;} else {inn=''+i;}
    inn=i;
    if (top1Menu){
      top1Menu.firstChild.className = "gnb-top-class-off";
      if (top2Menu) { top2Menu.style.display = 'none'; }
    }
  }
}

function initTopMenu() {
  top1menuEl = document.getElementById("top1menu").getElementsByTagName("ul");
  for (i=1;i<=top1menuEl.length;i++){
    top1Menu = document.getElementById("top1m"+i);
    top2Menu = document.getElementById("top2m"+i);
    if (top1Menu) {
      top1Menu.onmouseover = top1Menu.onfocus = top2menuView;
      top1Menu.onmouseout  = top2menuHide;
      if (top2Menu) {
        top2Menu.onmouseover = top2Menu.onfocus = top2menuView;
        top2Menu.onmouseout  = top2menuHide;
      }
    }
  }
}

function depth2over(a,b){ 
  var de2Str = document.getElementById("top2m"+a);
  var de2StrLi = de2Str.getElementsByTagName("li");
  for(var i=1;i<de2StrLi.length+6;i++){
    if(b==i){

    }
  }
}

function depth2out(a,b){
  var de2Str = document.getElementById("top2m"+a);
  var de2StrLi = de2Str.getElementsByTagName("li");
  for(var i=1;i<de2StrLi.length+6;i++){
    if(b==i){

    }
  }
}
function noDoubleClick(){
  
}
function pageGo(url){
  document.location.href=url;
}