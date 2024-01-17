import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BusquedaBdComponent } from './busqueda-bd.component';

describe('BusquedaBdComponent', () => {
  let component: BusquedaBdComponent;
  let fixture: ComponentFixture<BusquedaBdComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BusquedaBdComponent]
    });
    fixture = TestBed.createComponent(BusquedaBdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
