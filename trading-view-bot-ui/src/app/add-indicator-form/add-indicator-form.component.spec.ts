import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddIndicatorFormComponent } from './add-indicator-form.component';

describe('AddIndicatorFormComponent', () => {
  let component: AddIndicatorFormComponent;
  let fixture: ComponentFixture<AddIndicatorFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddIndicatorFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddIndicatorFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
