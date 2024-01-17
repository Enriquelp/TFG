import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BusquedaOnlineComponent } from './busqueda-online.component';

describe('BusquedaOnlineComponent', () => {
  let component: BusquedaOnlineComponent;
  let fixture: ComponentFixture<BusquedaOnlineComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BusquedaOnlineComponent]
    });
    fixture = TestBed.createComponent(BusquedaOnlineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
