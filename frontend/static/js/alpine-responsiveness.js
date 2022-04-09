const setup = () => {
  return {
    isSearchPanelOpen: false,
    openSearchPanel() {
      this.isSearchPanelOpen = true;
      this.$nextTick(() => {
        this.$refs.searchInput.focus();
      });
    },
    isMobileSubMenuOpen: false,
    openMobileSubMenu() {
      this.isMobileSubMenuOpen = true;
      this.$nextTick(() => {
        this.$refs.mobileSubMenu.focus();
      });
    },
    isMobileMainMenuOpen: false,
    openMobileMainMenu() {
      this.isMobileMainMenuOpen = true;
      this.$nextTick(() => {
        this.$refs.mobileMainMenu.focus();
      });
    },
  };
};

// let editor;
// document.onLoad = () => {
const editor = SUNEDITOR.create(document.getElementById("sample") || "sample", {
  lang: SUNEDITOR_LANG["en"],
});
// console.log(editor)
// }

// editor.onChange = (contents,core)=>{
//   console.log('onChange', contents)
// }

// const submit = document.getElementById('submit')

// submit.addEventListener('click',()=>{
//   console.log(editor.getText());
// })
// document.getElementsByTagName('body')[0].addEventListener('click',()=>{
// console.log(editor.getText());
// })
