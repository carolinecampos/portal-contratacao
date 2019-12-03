import { AbstractControl, AsyncValidator  } from '@angular/forms';
import { ContratoService } from '../contrato.service';
import { Blacklist } from '../../empresa/contratante.model';
import { of, Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
})

export class BlackListValidator implements AsyncValidator {

    static service: ContratoService;

    constructor(private __service: ContratoService) {
        BlackListValidator.service = __service;
    }

    validate(control: AbstractControl): Promise<{ [key: string]: any } | null>
    | Observable<{ [key: string]: any } | null> {
        return BlackListValidator.service.validarCNPJJaCadastrado(control.value).pipe(
            map(data => {
                let itemBlackList: Blacklist = new Blacklist();
                itemBlackList = data;
                if (Array.isArray(itemBlackList) && itemBlackList.length > 0) {
                    return ({ blackList: true});
                }
            }), catchError (error => of(null))
        );
        return of(null);
    }

}
