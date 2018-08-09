unit uwizardresetserverpassword_welcome;

{$mode objfpc}{$H+}

interface

uses
  uwizard,
  uwizardstepframe,
  Classes, SysUtils, FileUtil, Forms, Controls, StdCtrls, ExtCtrls;

type

  { TWizardResetServerPasswordWelcome }

  TWizardResetServerPasswordWelcome = class(TWizardStepFrame)
    image: TImage;
    lbl: TLabel;
    panel: TPanel;
  private

  public

    procedure wizard_load(w: TWizard); override; final;
    procedure wizard_show(); override; final;

  end;

implementation

uses
  LResources,
  resources;

{$R *.lfm}

{ TWizardResetServerPasswordWelcome }

procedure TWizardResetServerPasswordWelcome.wizard_load(w: TWizard);
begin
  inherited wizard_load(w);

  self.image.Picture.LoadFromLazarusResource(RES_IMG_WAPT);

end;

procedure TWizardResetServerPasswordWelcome.wizard_show();
begin
  inherited wizard_show();

  m_wizard.setFocus_async( self.m_wizard.WizardButtonPanel.NextButton );

end;

initialization

RegisterClass(TWizardResetServerPasswordWelcome);

end.

