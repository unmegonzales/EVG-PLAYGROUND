const DEPARTMENTS = [
  { code: '36127', name: 'Concessions' },
  { code: '36128', name: 'Group Sales' },
  { code: '36129', name: 'Suites (Culinary)' },
  { code: '57039', name: 'Warehouse' },
  { code: '34964', name: 'Admin' },
  { code: '34963', name: 'Management' },
  { code: 'NPO', name: 'Non-Profit Groups (NPO)' },
];

const CLASSIFICATIONS = [
  { id: 'levy_employee', label: 'Levy Employee' },
  { id: 'npo', label: 'Non-Profit Groups (NPO)' },
  { id: 'sub_vendor', label: 'Subcontractor (Vendors)' },
];

const SF_STAGES = [
  { id: 'new_employee', label: 'New Employee', waitingOn: 'candidate' },
  { id: 'orientation_step', label: 'Orientation Step', waitingOn: 'hr' },
  { id: 'signature_step', label: 'Signature Step', waitingOn: 'candidate' },
  { id: 'post_hire_verification', label: 'Post Hire Verification', waitingOn: 'hr' },
];

const PERMIT_STATUS = ['missing', 'no_match', 'uploaded', 'valid', 'expired', 'temporary'];
const UPLOAD_STATUS = ['missing', 'uploaded', 'validated'];
const I9_STATUS = ['not_started', 'section_1', 'section_2', 'complete', 'renewal_due'];
const CL_STATUS = ['missing', 'in_progress', 'complete'];

const FORM_LINKS = {
  alcohol: 'https://app.smartsheet.com/b/form/019f6f7922fc7fd1b5a526a2d01deab4',
  food: 'https://app.smartsheet.com/b/form/019fad237860724a9f910507aefed202',
  security: 'https://app.smartsheet.com/b/form/019fad23fc93785e85bef51c0bb5da2b',
  shirt: 'https://app.smartsheet.com/b/form/0198894ac22373d9a727ab2cb814f19a',
  creatingLegends: 'https://www.brainshark.com/levy/LevyTeamMemberCreatingLegends',
  digitalDen: 'https://app.smartsheet.com/b/publish?EQBCT=9742da38f8dd4f57867e905b1bfd6485',
};

module.exports = {
  DEPARTMENTS,
  CLASSIFICATIONS,
  SF_STAGES,
  PERMIT_STATUS,
  UPLOAD_STATUS,
  I9_STATUS,
  CL_STATUS,
  FORM_LINKS,
};
