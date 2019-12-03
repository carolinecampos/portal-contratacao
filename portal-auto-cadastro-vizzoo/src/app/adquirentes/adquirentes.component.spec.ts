import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdquirentesComponent } from './adquirentes.component';

describe('AdquirentesComponent', () => {
  let component: AdquirentesComponent;
  let fixture: ComponentFixture<AdquirentesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdquirentesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdquirentesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
