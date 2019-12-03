// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  test: false,
  stage: false,
  // URL_API: 'https://autoc-vizzo-core.cloudint.nexxera.com/autocontratacao',
  URL_API: 'http://127.0.0.1:8000/autocontratacao',
  URL_VIZZO: 'https://vizzoo-web-app-dev.cloudint.nexxera.com/vizzoo',
  API_LOGIN: 'autocontratacao',
  API_PASSWORD: 'autocvizzoo!',
  URL_LOGO: 'assets/img/logo-vizzoo.png',  
  URL_ICON_BOLETO: 'assets/img/barcode.png',
  URL_CONTRATO_PDF: 'assets/pdf/contrato-cliente-vizzoo.pdf',
  CEP_URL_API: 'https://address-repository-dev.cloudint.nexxera.com/api/v1/postal-code/',  
  URL_GERAR_BOLETO: 'https://gateway-nix-qa.cloudint.nexxera.com/v2/Orders/BoletoPayments/'
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
