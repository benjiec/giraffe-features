class Constant_Choices:

  @classmethod
  def choices(cls):
    choices = []
    for attr in dir(cls):
      v = getattr(cls, attr)
      if type(v) == type((1,2)):
        choices.append(v)
    return choices

  @classmethod
  def by_value(cls, value):
    for v in cls.choices():
      if v[0] == value:
        return v
    return (None, None)

  @classmethod
  def by_label(cls, label):
    for v in cls.choices():
      if v[1] == label:
        return v
    return (None, None)

  @classmethod
  def str(cls, value_or_tuple):
    if type(value_or_tuple) == type((1,2)):
      return value_or_tuple[1]
    else:
      return cls.by_value(value_or_tuple)[1]

  @classmethod
  def value(cls, str_or_tuple):
    if type(str_or_tuple) == type((1,2)):
      return str_or_tuple[0]
    else:
      return cls.by_label(str_or_tuple)[0]


class Feature_Type_Choices(Constant_Choices):

  FEATURE       = (1,  'Feature')
  PROMOTER      = (2,  'Promoter')
  PRIMER        = (3,  'Primer')
  ENZYME        = (4,  'Restriction Enzyme')
  GENE          = (5,  'Gene')
  ORIGIN        = (6,  'Origin')
  REGULATORY    = (7,  'Regulatory')
  TERMINATOR    = (8,  'Terminator')
  CUSTOM        = (9,  'Custom')
  ORF           = (10, 'Orf')
  PROTEIN       = (11, 'Protein')
  CUSTOM2       = (12, 'Custom2')
  CUSTOM3       = (13, 'Custom3')
  CUSTOM4       = (14, 'Custom4')

  @staticmethod
  def labels():
    return [t[1] for t in Feature_Type_Choices.choices()]


class Giraffe_Feature_Base(object):
  """
  Describes what part of a feature or subject matches to what part of a query
  sequence.

  Note that for coordinates, this class includes query_start and query_end, and
  subject_start and subject_end. All four values are 1-indexed bp positions on
  the forward strand. Therefore, if subject_start < subject_end, then the
  subject matches to the query, otherwise it matches to the reverse complement
  of the query.

  query_start and query_end always refers to bps on the forward strand of the
  query. If the query is circular, then query_start may be > query_end.

  It is more complicated when the query is linear, but the subject is circular,
  such as blasting a query against a circular genome. In this case,
  subject_start may be greater than subject_end across the circular boundary of
  the genome.

  To avoid confusion, software that wants to use this class to describe linear
  query matching to circular subject should stick to the convention that
  subject_start > subject_end implies matching subject to reverse complement of
  the query or matching reverse complement of subject to query. When presenting
  a match across the circular boundary of the subject, just use bp values
  greater than the circular length of the subject.
  """

  def __init__(self, label, name, query_start, query_end,
               subject_start, subject_end, type, layer):

    if type not in Feature_Type_Choices.labels():
      raise Exception("Invalid type: %s" % (type,))

    self.label = label
    self.name = name
    self.query_start = query_start
    self.query_end = query_end
    self.subject_start = subject_start
    self.subject_end = subject_end
    self.type = type
    self.layer = layer

  def to_dict(self):
    t = Feature_Type_Choices.by_label(self.type)
    return dict(label=self.label,
                name=self.name,
                query_start=self.query_start,
                query_end=self.query_end,
                subject_start=self.subject_start,
                subject_end=self.subject_end,
                type_id=t[0],
                layer=self.layer)


class Aligned_Feature(Giraffe_Feature_Base):

  def __init__(self, accession, name,
               query_start, query_end, subject_start, subject_end, type,
               alignment_query, alignment_match, alignment_subject,
               evalue, identities):

    super(Aligned_Feature, self).__init__(accession, name, query_start, query_end,
                                          subject_start, subject_end, type, 'Detected Features')
    self.alignment_query = alignment_query
    self.alignment_match = alignment_match
    self.alignment_subject = alignment_subject
    self.evalue = evalue
    self.identities = identities

  def to_dict(self):
    r = super(Aligned_Feature, self).to_dict()
    r['alignment'] = { 'query': self.alignment_query,
                       'match': self.alignment_match,
                       'subject': self.alignment_subject }
    r['evalue'] = self.evalue
    r['identities'] = self.identities
    return r
