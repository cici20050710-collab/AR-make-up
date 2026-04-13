function selectCategory(cat){
    currentCategory = cat;

    // 清掉全部樣式
    document.getElementById("btn-base").classList.remove("text-pink-600");
    document.getElementById("btn-eye").classList.remove("text-pink-600");
    document.getElementById("btn-lip").classList.remove("text-pink-600");

    // 高亮目前選擇
    if(cat==="底妝") document.getElementById("btn-base").classList.add("text-pink-600");
    if(cat==="眼妝") document.getElementById("btn-eye").classList.add("text-pink-600");
    if(cat==="唇妝") document.getElementById("btn-lip").classList.add("text-pink-600");

    console.log("目前選擇:", cat);
}